from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import UserexistError
from app.models import User
from app.libs.rewrite import BaseForm as Form

class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(min=5, max=32)])
    password = StringField()
    type = IntegerField(validators=[DataRequired()], default=100)

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client

class UserEmailForm(ClientForm):
    account = StringField(validators=[DataRequired(), Email(message='Invalid email')])
    password = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise UserexistError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])