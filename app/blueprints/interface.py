from flask import Blueprint

inter_bp = Blueprint('inter_bp',__name__)

@inter_bp.route('/interface')
def interface():
    pass
