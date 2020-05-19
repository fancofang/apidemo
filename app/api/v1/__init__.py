from flask import Blueprint

from app.api.v1.auth import auth

api_v1 = Blueprint('v1',__name__)

from . import user, client, book

@api_v1.before_request
@auth.login_required()
def before_request():
    pass
