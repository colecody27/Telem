from app.extensions import db, jwt 
from flask import Flask
from app.logger import init_app
from app.config import Config, ProductionConfig, DevelopmentConfig
import os

def create_app():
    app = Flask(__name__)
    init_app(app) # Logging

    # Choose config based on environment
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

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