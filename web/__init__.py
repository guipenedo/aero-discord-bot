from flask import Flask, request
from bot import fenix_client, auth_sucess

from database import Session, engine, Base, User

Base.metadata.create_all(engine)
session = Session()

app = Flask(__name__)


@app.route('/')
def auth():
    if 'error' in request.args:
        return f"{request.args.get('error')}: {request.args.get('error_description')}"
    try:
        if 'code' not in request.args:
            raise Exception()
        code = request.args.get('code')
        user_id = int(request.args.get('state'))
        user_info = fenix_client.get_user_by_code(code)
    except:
        return "Erro ao tentar obter um access token. Por favor tente novamente."
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
    user = User(user_id, user_info.access_token, user_info.refresh_token, user_info.token_expires)
    session.add(user)
    session.commit()
    return "Sucesso. Já pode fechar esta página."
