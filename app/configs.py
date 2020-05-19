import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config():
    SECRET_KEY =os.getenv('SECRET_KEY', 'api_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_BINDS = {'book': 'mysql://' + os.getenv('MYSQL_USER', 'root') \
                                + ':' + os.getenv('MYSQL_PASSWORD', '')\
                                + '@localhost:3306/book'}



class ProductionConfig(Config):
    pass



config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}