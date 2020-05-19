from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from flask_oauthlib.client import OAuth
# from authlib.flask.client import OAuth
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()
