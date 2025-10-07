import re
from app.models import User

def is_email_valid(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return False, {'error': 'Account with this email already exists'}
    if not re.fullmatch("[^@]+@[^@]+\.[^@]+", email):
        return False, {'error': 'Invalid email'}
    return True, {}

def is_password_valid(password):
    if len(password) < 8:
        return False, {'error': 'Password must have at least 8 characters'}
    if password.islower():
        return False, {'error': 'Password must have at least 1 upper case character'}
    if password.isalpha():
        return False, {'error': 'Password must have at least 1 number'}
    if password.isalnum():
        return False, {'error': 'Password must have at least 1 special characters'}
    return True, {}

def is_username_valid(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return False, {'error': 'Username already exists'}
    return True, {}

# Validate email exist 
def is_user(email):
    return True if User.query.filter_by(email=email).first() else False