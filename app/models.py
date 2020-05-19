from datetime import datetime

from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_login import UserMixin

from app.libs.enums import ScopeTypeEnum
from app.libs.error_code import NotFound, AuthFailed, UserexistError


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True, nullable=False)
    auth = db.Column(db.Integer, default=1)
    register_from = db.Column(db.String(24), default='email')
    _password = db.Column(db.String(128))

    @orm.reconstructor
    def __init__(self, **kw):
        super(User, self).__init__(**kw)
        self.fields = ['id', 'email', 'auth', 'register_from']


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)


    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def __getitem__(self, item):
        return getattr(self, item)

    def validate_password(self, password):
        return check_password_hash(self._password, password)

    @staticmethod
    def verify(email,password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound()
        if user.password is None:
            msg = 'User already exists, registered from %s' %user.register_from
            raise UserexistError(msg=msg)
        if not user.validate_password(password):
            raise AuthFailed()
        scope =ScopeTypeEnum(user.auth).name
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid':user.id, 'scope':scope}

    @staticmethod
    def verify_oauth(email):
        user = User.query.filter_by(email=email).first()
        scope =ScopeTypeEnum(user.auth).name
        # scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid':user.id, 'scope':scope}


class Book(db.Model):
    __bind_key__ = 'book'
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    authors = db.Column(db.String(50), nullable="Null")
    average_rating = db.Column(db.String(50))
    isbn = db.Column(db.String(15), nullable=False, unique=True)
    isbn13 = db.Column(db.String(20))
    language_code = db.Column(db.String(15))
    num_pages = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    text_reviews_count = db.Column(db.Integer)
    publication_date = db.Column(db.DateTime)
    publisher = db.Column(db.String(50))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'title', 'authors', 'average_rating',
                'isbn', 'isbn13', 'language_code', 'num_pages',
                'ratings_count', 'text_reviews_count', 'publication_date', 'publisher'
        ]

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def __getitem__(self, item):
        return getattr(self, item)
