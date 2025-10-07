from flask import Blueprint, request, jsonify
from app.services import auth_service
from app.extensions import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# GET
@auth_bp.route('/me')
@jwt_required()
def get_user():
    id = get_jwt_identity()
    user = auth_service.get_user(id)
    
    if not user:
        return jsonify({'error': 'User does not exist'})
    
    return jsonify(user)


# POST
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Validate email/password exist 
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 401
    
    # Verify account
    token = auth_service.authenticate_user(email, password)
    if 'error' in token:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify(access_token=token)


# POST
@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    if not email or not username or not password:
        return jsonify({'error': f'Email, username, and password are required'})
    
    error = auth_service.register_user(email=email, username=username, password=password)
    if 'error' in error:
        return jsonify(error)
    return jsonify({'message': f'User has been registered successfully'})