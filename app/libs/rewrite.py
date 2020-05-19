from wtforms import Form
from app.libs.error_code import ParameterException, ServerError
from flask.json import JSONEncoder as _JSONEncoder
from flask import Flask as _Flask


class BaseForm(Form):
    def __init__(self, data):
        super(BaseForm, self).__init__(data=data)
        pass

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        try:
            val = super(JSONEncoder, self).default(o)
            return val
        except:
            if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
                return dict(o)
        raise ServerError()

class Flask(_Flask):
    json_encoder = JSONEncoder
