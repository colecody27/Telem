from app.extensions import db, jwt 
from flask import Flask
from app.logger import init_app
from app.config import Config

def create_app():
    app = Flask(__name__)
    init_app(app) # Logging
    app.config.from_object(Config) # Environment configurations
    db.init_app(app) # Connect database 
    jwt.init_app(app) # Connect JWT

    # Connect blueprints 
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.alerts import alert_bp
    app.register_blueprint(alert_bp)
    from app.routes.sensors import sensor_bp
    app.register_blueprint(sensor_bp)

    return app