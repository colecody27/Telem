from app.extensions import db
from enum import Enum 
from sqlalchemy import Enum
from datetime import datetime

class SeverityLevel(Enum):
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'

class Alert(db.Model):
    __tablename__ = 'Tables'

    id = db.Column(db.Integer, primary_key=True),
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id', ondelete='CASCADE'), nullable=False)
    severity = db.Column(Enum(SeverityLevel, native_enum=False), nullable=False)
    ack = db.Column(db.Boolean, default=False)
    ack_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    sensor = db.relationship("Sensor", back_populates="alerts")
    ack_by_user = db.relationship("User", back_populates="alerts_ack")


class Sensor(db.Model):
    __tablename__ = 'Sensors'

    id = db.Column(db.Integer, primary_key=True),
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False),
    type = db.Column(db.String(50), nullable=False)
    ack = db.Column(db.Boolean, default=False)
    ack_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    sensor = db.relationship("Sensor", back_populates="alerts")
    ack_by_user = db.relationship("User", back_populates="alerts_ack")


    """
    id
    name
    type
    owner id
    location
    is_active
    created_at
    description
    """

class Sensor_Data(db.Model):
    __tablename__ = 'Sensor_Data'

    """
    id
    sensor id
    value
    unit
    created_at
    """

class User(db.Model):
    __tablename__ = 'Users'

    """
    id
    username
    email
    password_hash
    role
    created_at
    """