from app.extensions import db
from enum import Enum as PyEnum 
from sqlalchemy import Enum as SQLEnum
from datetime import datetime

class SeverityLevel(PyEnum):
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'

class Role(PyEnum):
    ENGINEER = 'engineer'
    ADMIN = 'admin'

class Alert(db.Model):
    __tablename__ = 'Alerts'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id', ondelete='CASCADE'), nullable=False)
    severity = db.Column(SQLEnum(SeverityLevel, native_enum=False), nullable=False)
    ack = db.Column(db.Boolean, default=False)
    ack_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    sensor = db.relationship("Sensor", back_populates="alerts")
    ack_by_user = db.relationship("User", back_populates="alerts_ack")

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "severity": self.severity.value,
            "ack": self.ack,
            "ack_by": self.ack_by,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Sensor(db.Model):
    __tablename__ = 'Sensors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    ack = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship("User", back_populates="sensors")
    sensor_data = db.relationship("Sensor_Data", back_populates="sensor")
    alerts = db.relationship("Alert", back_populates="sensor")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "ack": self.ack,
            "ack_by": self.ack_by,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Sensor_Data(db.Model):
    __tablename__ = 'Sensor_Data'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    sensor = db.relationship("Sensor", back_populates="sensor_data")

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "value": self.value,
            "unit": self.unit,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), default=False)
    role = db.Column(SQLEnum(Role, native_enum=False), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,  # Enum -> string
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    sensors = db.relationship("Sensor", back_populates="user")
    alerts_ack = db.relationship("Alert", back_populates="ack_by_user")
