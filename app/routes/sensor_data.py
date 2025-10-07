from flask import Blueprint

sensor_data_bp = Blueprint('sensor_data', __name__, url_prefix='/api/sensors/<id>/data')

# POST 
@sensor_data_bp.route(methods=['POST'])
def create_sensor(id=None):
    pass

# TODO Add query params 
# GET
@sensor_data_bp.route('/&')
def get_sensors():
    pass

# GET
@sensor_data_bp.route('/latest')
def get_sensor(id=None):
    pass

# DELETE
@sensor_data_bp.route(methods=['DELETE'])
def remove_sensor(id=None):
    pass