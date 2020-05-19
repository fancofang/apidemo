from flask import jsonify, g

from app.api.v1.auth import auth
from app.extensions import db
from app.libs.error_code import NotFound, Delete
from app.models import User
from . import api_v1



@api_v1.route('/user', methods=['GET'])
def get_user():
    """
    Get user detail

    :url: http://127.0.0.1:5000/api/v1/user
    :method: GET
    :authorization: Bearer
    :return: return email, register from and authorization
    """
    print(auth.current_user())
    user = User.query.get_or_404(g.user.uid)
    if not user:
        raise NotFound()
    user = user.hide('id')
    return jsonify(user)

@api_v1.route('/user', methods=['PATCH'])
def update_user():
    user = User.query.get_or_404(g.user.uid)
    if not user:
        raise NotFound()
    return jsonify(user)

@api_v1.route('/user', methods=['DELETE'])
def delete_user():
    """
    Delete user

    :url: http://127.0.0.1:5000/api/v1/user
    :method: DELETE
    :authorization: Bearer
    :return: delete the current user, return success
    """
    user = User.query.get_or_404(g.user.uid)
    if not user:
        raise NotFound()
    db.session.delete(user)
    db.session.commit()
    return Delete()

@api_v1.route('/user/<int:uid>', methods=['GET'])
def super_get_user(uid):
    user = User.query.get_or_404(uid)
    if not user:
        raise NotFound()
    return jsonify(user)

@api_v1.route('/users', methods=['GET'])
def super_get_users(uid):
    user = User.query.get_or_404(uid)
    if not user:
        raise NotFound()
    return jsonify(user)