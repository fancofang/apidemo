from app.libs.error_code import TokenFailed
from app.libs.token import verify_auth_token
from flask import g, request
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    if request.endpoint == 'v1.get_token' or request.endpoint == 'v1.create_client':
        # raise AuthFailed()
        return True
    if not 'Authorization' in request.headers:
        raise TokenFailed()
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return user_info

