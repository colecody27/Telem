from app.extensions import db, jwt
from app.models import User, Role
from flask_jwt_extended import create_access_token
import bcrypt
from app.utils import *
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger

def get_user(id):
    """
    Get user information from databse

    Args:
        id (Integer): ID of user which is the Primary key for Users table

    Returns:
        dict (dict): Dictionary translation of the returned User object with some fields redacted such as password
        None: Returns None if user isn't found 
    
    """
    user = User.query.get(id)
    return user.to_dict() if user else None

# Validate credentials and return JWT
def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    
    if not user:
        logger.info(f'Authentication of user with email: {email} as failed since email DNE')
        return {'error': f'User with email {email} does not exist, plaese register'}
    if email != user.email or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        print(f'Provided pw: {password.encode("utf-8")} Stored PW: {user.password_hash}')
        logger.info(f'Authentication of user with email: {email} as failed')
        return {'error': f'Email or password is incorrect'}
    
    token = create_access_token(identity=str(user.id))
    logger.info(f'User with email: {email} has been authenticated')
    return token

# Revoke token 
def logout_user():
    pass

# Create user
def register_user(email, username, password, role=Role.ENGINEER):
    # Email 
    is_valid, msg = is_email_valid(email)
    if not is_valid:
        logger.info(f'Failed to register user with email: {email}')
        return msg
    
    # Username
    is_valid, msg = is_username_valid(username)
    if not is_valid:
        logger.info(f'Failed to register user with username: {username}')
        return msg
    
    # Password
    is_valid, msg = is_password_valid(password)
    if not is_valid:
        logger.info(f'Failed to register user with email: {email}, due to password restrictions')
        return msg
    
    password_hash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt()).decode('utf-8')
    user = User(email=email, username=username, password_hash=password_hash, role=role)
    try:
        db.session.add(user)
    except SQLAlchemyError as e:
        logger.error(f'Error registering user with: {user} in database')
        return {'error': 'Internal service error'}
    
    db.session.commit()
    return {}





    

