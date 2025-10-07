from flask import Blueprint

sensor_bp = Blueprint('sensors', __name__, url_prefix='/api/sensors/')

# POST 
@sensor_bp.route(methods=['POST'])
def create_sensor():
    pass

# GET
@sensor_bp.route('')
def get_sensors():
    pass

# GET
@sensor_bp.route('/api/sensors/<id>')
def get_sensor(id=None):
    pass

# PUT
@sensor_bp.route('/api/sensors/<id>', methods=['PUT'])
def update_sensor(id=None):
    pass

# DELETE
@sensor_bp.route('/api/sensors/<id>', methods=['DELETE'])
def remove_sensor(id=None):
    pass