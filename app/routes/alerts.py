from flask import Blueprint

alert_bp = Blueprint('alert', __name__, url_prefix='/api/alerts')

# GET
@alert_bp.route('')
def get_alerts():
    pass

# GET
@alert_bp.route('/<id>')
def get_alert(id=None):
    pass

# PUT
@alert_bp.route('/<id>/ack')
def ack_alert(id=None):
    pass