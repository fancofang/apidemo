import json

from flask import Blueprint, jsonify, render_template

from app import db
from app.models import User

index_bp = Blueprint('bp',__name__)

@index_bp.route('/')
def index():
    """Index

    :url: http://3.9.215.67:9999/
    """
    return jsonify({
        "api_version": "1.0",
        "documentation": "http://3.9.215.67:9999/doc/index.html",
        "api_base_url": "http://3.9.215.67:9999/api/v1",
        "website_log_in_url": "http://3.9.215.67:9999/login",
        "api_register_url": "http://3.9.215.67:9999/api/v1/register",
        "api_get_token_url": "http://3.9.215.67:9999/api/v1/token",
        "api_current_user_url": "http://3.9.215.67:9999/api/v1/user",
        "api_item_search_url": "http://3.9.215.67:9999/api/v1/book/search?q={name}",
        "api_item_detail_url": "http://3.9.215.67:9999/api/v1/book/{isbn or isbn13}"
    })


# @index_bp.route('/documentation')
# def documentation():
#     return render_template('html/index.html')

@index_bp.route('/test')
def get_admin_account():
    admin = User(
        email='test@hotmail.com',
        auth=2
    )
    admin.password = '12345678'
    db.session.add(admin)
    db.session.commit()
