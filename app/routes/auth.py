from flask import Blueprint, request, jsonify
from app.services import auth_service
from app.extensions import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# GET
@jwt_required()
@auth_bp.route('/me')
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
    
    # Verify email exist
    is_user = auth_service.is_user(email)
    if not is_user:
        return jsonify({'error': f'User with email {email} does not exist, plaese register'})
    
    # Verify account
    token = auth_service.authenticate_user(email, password)
    if not token:
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
    
    auth_service.register_user(email=email, username=username, password=password)
    return jsonify({'message': f'User has been registered successfully'})