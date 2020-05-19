from flask import render_template, Blueprint, request, jsonify, redirect, url_for

from app.extensions import db
from app.libs.error_code import UserexistError
from app.libs.token import generate_auth_token, combine_token_info
from app.models import User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']
        identity = User.verify(email, password)
        token, expires_in = generate_auth_token(identity['uid'],
                                                identity['scope'],
                                                expiration=1800)
        t = combine_token_info(token, expires_in, scope=identity['scope'] )
        return jsonify(t), 201
    return render_template('_login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            user.password = password
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('.login'))
        return UserexistError()
    return render_template('_register.html')
