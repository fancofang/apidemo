from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'Ok'
    error_code = 0

class Delete(APIException):
    code = 202
    msg = 'Delete success'
    error_code = 1

class ServerError(APIException):
    pass

class ParameterException(APIException):
    code = 400
    msg = 'Invaild parameter'
    error_code = 999

class UserexistError(APIException):
    code = 400
    msg = 'User already exists'
    error_code = 1000

class NotFound(APIException):
    code = 404
    msg = 'User not found'
    error_code = 1001

class AuthFailed(APIException):
    code = 401
    msg = 'Authorization failed'
    error_code = 1002

class Forbidden(APIException):
    code = 403
    msg = 'Forbidden'
    error_code = 1100

class Tokeninvalid(APIException):
    code = 400
    msg = 'Token is invalid'
    error_code = 1003

class Tokenexpired(APIException):
    code = 400
    msg = 'Token is invalid'
    error_code = 1004


class BookException(APIException):
    code = 400
    msg = 'Can`t find the result'
    error_code = 1006

class TokenFailed(APIException):
    code = 401
    msg = 'Miss token'
    error_code = 1005