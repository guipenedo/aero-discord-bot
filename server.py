#server
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from urllib import parse
#database
from database import Session, engine, Base, discordUser




Base.metadata.create_all(engine)
session = Session()

#Server ------------------------------------

PORT = 80      



class StaticServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        filename = 'form.html'

        with open(filename, 'rb') as fh:
            html = fh.read()
            self.wfile.write(html)

    def do_POST(self):
        parsed_path = parse.urlparse(self.path)
        message = parsed_path.query
        code = message[5:]
        content_length = int(self.headers['Content-Length'])
        data_input = bytes.decode(self.rfile.read(content_length), 'iso-8859-1')
        u = data_input[8:]


        if '&#' in u:
            message = 'O seu username contém caracteres especiais não reconhecidos por este servidor. Pedimos desculpa por este incómodo. Por favor contacte um membro do NEEC de forma a proceder à resolução deste problema.'
            self.send_response(200)

            self.send_header('Content-Type',
                            'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

            return

        #verificar se já está na database, e eleminá-lo nesse caso
        users = session.query(discordUser).all() 
        for x in users:
            # print(len(str(x.discordUsername[:-2])))
            # print(len(str(u[:-2])))
            # print(x.discordUsername)
            if((str(x.discordUsername[:-2]) == str(u[:-2]))):
                print('igual')
                session.delete(x)
                
        
        # print (u)
        user = discordUser(u, None, None, None, code)
        session.add(user)
        session.commit()

        message = 'O seu username foi gravado. Pode fechar esta janela.'

        self.send_response(200)

        self.send_header('Content-Type',
                        'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    
def run(server_class=HTTPServer, handler_class=StaticServer):
    server_address = ("", PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

while True:
    run()



   
