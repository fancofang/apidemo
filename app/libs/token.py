import time

from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request
from app.libs.error_code import Forbidden, Tokeninvalid, Tokenexpired
from app.libs.scope import is_in_scope


User = namedtuple('User', ['uid', 'ac_type', 'scope'])


# 生成令牌
def generate_auth_token(uid, ac_type='Email', scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type,
        'scope': scope
    }), time.time() + expiration


#验证令牌
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise Tokeninvalid()
    except SignatureExpired:
        raise Tokenexpired()
    uid =data['uid']
    type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, type, scope)



def combine_token_info(token, exp , authorization='Bearer', scope='UserScope'):
    t = {
        'Token': token.decode('ascii'),
        'Authorization': authorization,
        'Scope': scope,
        'Expire_in': time.strftime("%d %b %Y %H:%M:%S Localtime", time.localtime(exp)),
    }
    return t