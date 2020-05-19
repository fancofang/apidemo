from flask import request, jsonify
from app.models import User
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.token import generate_auth_token, combine_token_info
from . import api_v1
from app.forms import ClientForm, UserEmailForm
from app.extensions import db


@api_v1.route('/register', methods=['POST'])
def create_client():
    """
    Register user

    :url: http://127.0.0.1:5000/api/v1/register
    :method: POST
    :param: account, password
    :return: return result
    :example: {
            "account": "guest@hotmail.com",
            "password":"12345678"}
    """
    form = ClientForm(data=request.json)
    form.validate_for_api()
    switch = {
        ClientTypeEnum.Email:_register_user_by_email,
    }
    switch[form.type.data]()
    return Success()

def _register_user_by_email():
    form = UserEmailForm(data = request.json)
    form.validate_for_api()
    user = User(
        email=form.account.data,
        password=form.password.data
    )
    db.session.add(user)
    db.session.commit()





@api_v1.route('/token', methods=['POST'])
def get_token():
    """
    Get user token

    :url: http://127.0.0.1:5000/api/v1/token
    :method: POST
    :param: account, password
    :return: return token, expiration, scope
    :example: {
        "Authorization": "Bearer",
        "Expire_in": "12 Jun 2020 21:35:23 Localtime",
        "Scope": "UserScope",
        "Token": "eyJlA..."}
    """
    form = ClientForm(data=request.json)
    form.validate_for_api()
    switch = {
        ClientTypeEnum.Email: User.verify,
    }
    identity = switch[form.type.data](
        form.account.data,
        form.password.data
    )
    expiration = 30 * 24 * 3600
    token, expires_in = generate_auth_token(identity['uid'],
                                form.type.data.name,
                                identity['scope'],
                                expiration)
    t = combine_token_info(token, expires_in, scope=identity['scope'])
    return jsonify(t),201