from app import create_app

# Create the Flask app using the factory pattern
app = create_app()

# Example: gunicorn --bind 0.0.0.0:5000 wsgi:app
