import os

class Config:
    # General
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev_jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # seconds (1 hour)
