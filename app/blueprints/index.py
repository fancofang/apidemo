from flask import Blueprint, jsonify

from app import db
from app.models import User

index_bp = Blueprint('bp',__name__)

@index_bp.route('/')
def index():
    return jsonify({
        "api_version": "1.0",
        "api_base_url": "http://127.0.0.1:5000/api/v1",
        "website_log_in_url": "http://127.0.0.1:5000/login",
        "api_register_url": "http://127.0.0.1:5000/api/v1/register",
        "api_get_token_url": "http://127.0.0.1:5000/api/v1/token",
        "api_current_user_url": "http://127.0.0.1:5000/api/v1/user",
        "api_item_search_url": "http://127.0.0.1:5000/api/v1/book/search?q={name}",
        "api_item_detail_url": "http://127.0.0.1:5000/api/v1/book/{isbn or isbn13}"
    })


@index_bp.route('/test')
def get_admin_account():
    admin = User(
        email='test@hotmail.com',
        auth=2
    )
    admin.password = '12345678'
    db.session.add(admin)
    db.session.commit()