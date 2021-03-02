import config
from flask import Flask, request
from fenix import fenix_client

from database import session_scope, User, init_db

app = Flask(__name__)
init_db()


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
        return config.WEB_ERROR
    with session_scope() as session:
        user = session.query(User).get(user_id)
        if user:
            user.access_token = user_info.access_token
            user.refresh_token = user.refresh_token
            user.new_semester = True
        else:
            user = User(user_id, user_info.access_token, user_info.refresh_token, user_info.token_expires)
            session.add(user)
        return config.WEB_SUCCESS
