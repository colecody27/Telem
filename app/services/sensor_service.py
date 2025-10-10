from app.extensions import db
from app.models import Sensor
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger

def create_sensor(user_id, type, latitude=None,
                  longitude=None, is_active=False,
                  description=None):
    """
    Create and persist a new Sensor.

    Returns the created sensor as a dict, or an error dict on failure.
    """

    sensor = Sensor(
        user_id=user_id,
        type=type,
        latitude=latitude,
        longitude=longitude,
        is_active=is_active,
        description=description,
    )

    try:
        db.session.add(sensor)
        db.session.commit()
        logger.info(f"Created sensor id={sensor.id} for user_id={user_id}")
        return sensor.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error creating sensor for user {user_id}: {e}")
        return {"error": "Internal service error"}


def get_sensors(user_id=None):
    """Return a list of sensors. If user_id is provided, filter by that user."""
    try:
        if user_id is not None:
            sensors = Sensor.query.filter_by(user_id=user_id).all()
        else:
            sensors = Sensor.query.all()
        return [s.to_dict() for s in sensors]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching sensors: {e}")
        return None


def get_sensor(sensor_id):
    """Return a sensor dict by id or None if not found."""
    try:
        sensor = Sensor.query.get(sensor_id)
        return sensor.to_dict() if sensor else None
    except SQLAlchemyError as e:
        logger.error(f"Error fetching sensor {sensor_id}: {e}")
        return None


def update_sensor(sensor_id, **fields):
    """Update allowed sensor fields and return the updated dict, or None on not found/error."""
    allowed = {"type", "latitude", "longitude", "is_active", "description", "ack", "ack_by"}
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            logger.info(f'Sensor with {sensor_id} does not exist')
            return None

        for key, value in fields.items():
            if key not in allowed:
                logger.info(f'Attempted to update {key} on sensor {sensor_id}. Skipping.')
                continue
            else:
                setattr(sensor, key, value)

        db.session.commit()
        logger.info(f'Successfully updated sensor {sensor_id}')
        return sensor.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error updating sensor {sensor_id}: {e}")
        return None


def delete_sensor(sensor_id):
    """Delete sensor by id. Returns True on success, False otherwise."""
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return False
        db.session.delete(sensor)
        db.session.commit()
        logger.error(f"Successfully deleted sensor {sensor_id}")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error deleting sensor {sensor_id}: {e}")
        return False
