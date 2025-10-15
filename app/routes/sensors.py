from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import auth_service, sensor_service
from app.models import Sensor
from app.utils import *

sensor_bp = Blueprint('sensors', __name__, url_prefix='/api/sensors/')

# POST 
@sensor_bp.route('', methods=['POST'])
@jwt_required()
def create_sensor():
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)

    if not user:
        return jsonify({'error': 'User does not exist'})
    
    data = request.get_json()
    type = data.get('type')
    is_valid_lat, latitude = to_float(data.get('latitude'))
    is_valid_long, longitude = to_float(data.get('longitude'))
    is_valid_active, is_active = to_boolean(data.get('is_active'))
    description = data.get('description')

    if not type:
        return jsonify({'error': 'Sensor type must be provided'})
    
    if not is_valid_lat or not is_valid_long:
        return jsonify({'error': 'Latitude ang longitude coordinates must be valid numbers'})
    
    if not is_valid_active:
        return jsonify({'error': 'is_active must be true or false'})
    
    sensor = sensor_service.create_sensor(user_id=user_id, type=type, latitude=latitude, longitude=longitude, is_active=is_active, description=description)
    if 'error' in sensor:
        return jsonify({'error': f'Error creating sensor'}), 500
    
    return jsonify(sensor)

# GET
@sensor_bp.route('', methods=['GET'])
@jwt_required()
def get_sensors():
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)

    if not user:
        return jsonify({'error': 'User does not exist'})    
    
    sensors = sensor_service.get_sensors(user_id)
    if sensors is None:
        return jsonify({'error': f'Error fetching sensors'}), 500
    
    return jsonify(sensors)

# GET
@sensor_bp.route('/<sensor_id>', methods=['GET'])
@jwt_required()
def get_sensor(sensor_id=None):
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)
    if not sensor_id or not sensor_id.isnumeric():
        return jsonify({'error': f'Invalid sensor id'})

    if not user:
        return jsonify({'error': 'User does not exist'}) 
    if not Sensor.query.filter_by(user_id=user_id, id=sensor_id).first():
        return jsonify({'error': 'Sensor does not exist'})    
    
    sensor = sensor_service.get_sensor(user_id)
    if not sensor:
        return jsonify({'error': f'Error fetching sensor'}), 500
    
    return jsonify(sensor)

# TODO - GET all data for every sensor

# PUT
@sensor_bp.route('', methods=['PUT'])
@jwt_required()
def update_sensor():
    id = get_jwt_identity()
    user = auth_service.get_user(id)
    data = request.get_json()
    sensor_id = data.get('id')

    if not sensor_id or not sensor_id.isnumeric():
        return jsonify({'error': f'Invalid sensor id'})
    if not user:
        return jsonify({'error': 'User does not exist'})   
    if not sensor_id or not Sensor.query.filter_by(id=sensor_id, user_id=id).first():
        return jsonify({'error': 'Sensor does not exist'})   
    
    type = data.get('type')
    is_valid_lat, latitude = to_float(data.get('latitude'))
    is_valid_long, longitude = to_float(data.get('longitude'))
    is_valid_active, is_active = to_boolean(data.get('is_active'))
    description = data.get('description')

    if not is_valid_lat or not is_valid_long:
        return jsonify({'error': 'Latitude ang longitude coordinates must be valid numbers'})
    if not is_valid_active:
        return jsonify({'error': 'is_active must be "true" or "false"'})
    
    update_sensor_request = {'type': type, 'latitude': latitude, 'longitude': longitude, 'is_active': is_active, 'description': description}
    updated_sensor = sensor_service.update_sensor(sensor_id, update_sensor_request)

    if not updated_sensor:
        return jsonify({'error': f'Error updating sensor'}), 500
    
    return jsonify(updated_sensor)

# DELETE
@sensor_bp.route('/<sensor_id>', methods=['DELETE'])
@jwt_required()
def remove_sensor(sensor_id=None):
    id = get_jwt_identity()
    user = auth_service.get_user(id)

    if not user:
        return jsonify({'error': 'User does not exist'}) 
    if not sensor_id or not Sensor.query.filter_by(id=sensor_id, user_id=id).first():
        return jsonify({'error': 'Sensor does not exist'})
    
    deleted = sensor_service.delete_sensor(sensor_id)
    if not deleted:
        return jsonify('error' f'Error deleting sensor'), 500
    
    return jsonify({'msg': f'Sensor {sensor_id} has been deleted'})

# POST 
@sensor_bp.route('/<sensor_id>/data', methods=['POST'])
@jwt_required()
def add_sensor_data(sensor_id=None):
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)
    data = request.get_json()

    if data.get('value') is None or data.get('unit') is None:
        return jsonify({'error': 'Value and unit must be provided'})
    if not user:
        return jsonify({'error': 'User does not exist'})
    
    data_log = sensor_service.log_sensor_data(user_id=user_id, sensor_id=sensor_id, data=data)

    if 'error' in data_log:
        return jsonify(data_log), 500
    
    return jsonify(data_log)

# GET
@sensor_bp.route('/<sensor_id>/data', methods=['GET'])
@jwt_required()
def get_sensor_data(sensor_id=None):
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User does not exist'})    
    
    sensor_data = sensor_service.get_sensor_data(user_id=user_id, sensor_id=sensor_id)
    return jsonify(sensor_data)

# DELETE
@sensor_bp.route('/<sensor_id>/data/<data_id>', methods=['DELETE'])
@jwt_required()
def remove_sensor_data(sensor_id=None, data_id=None):
    user_id = get_jwt_identity()
    user = auth_service.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User does not exist'}) 
    
    deleted_data = sensor_service.remove_sensor_data(sensor_id=sensor_id, user_id=user_id, data_id=data_id)
    return jsonify(deleted_data)