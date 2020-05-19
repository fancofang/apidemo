import os
import click
from app.libs.rewrite import Flask
from werkzeug.exceptions import HTTPException

from app.configs import config
from app.api import v1

from app.extensions import db, oauth
from app.libs.error import APIException
from app.libs.error_code import ServerError


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)

    return app


def register_blueprints(app):
    from app.blueprints.index import index_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.oauth import oauth_bp

    app.register_blueprint(v1.api_v1, url_prefix='/api/v1')
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(oauth_bp, url_prefix='/oauth')

def register_extensions(app):
    db.init_app(app)
    oauth.init_app(app)

def register_commands(app):

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        from app.models import User
        if drop:
            click.confirm('Sure?', abort=True)
            db.drop_all()
            click.echo('Drop all tables')
        db.create_all()
        click.echo('Initialized database')

    @app.cli.command()
    def createadmin():
        from app.models import User
        admin = User(
            email='fanghao23@hotmail.com',
            auth=2
        )
        admin.password = '123456'
        db.session.add(admin)
        db.session.commit()
        click.echo('Create admin account')

def register_errors(app):
    @app.errorhandler(Exception)
    def whole_error(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 1007
            return APIException(msg, code, error_code)
        else:
            if app.config['DEBUG']:
                raise e
            else:
                return ServerError()

