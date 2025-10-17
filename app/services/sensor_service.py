from app.extensions import db
from app.models import Sensor, Sensor_Data, Unit
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.utils import *

def create_sensor(user_id, type, latitude=None,
                  longitude=None, is_active=True,
                  description=None):

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


def update_sensor(sensor_id, fields):
    """Update allowed sensor fields and return the updated dict, or None on not found/error."""
    allowed = {"type", "latitude", "longitude", "is_active", "description"}
    try:
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            logger.info(f'Sensor with {sensor_id} does not exist')
            return None

        for key, value in fields.items():
            if key not in allowed:
                logger.info(f'Attempted to update {key} on sensor {sensor_id}. Skipping.')
                continue
            elif value != None:
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

def log_sensor_data(user_id, data):
    readings_added = []
    for reading in data:
        sensor_id = reading.get("sensor_id")
        unit = reading.get("unit")
        value = reading.get("value") 
        sensor = Sensor.query.filter_by(id=sensor_id, user_id=user_id).first()
        if not sensor:
            logger.info(f"Sensor {sensor_id} not found for user {user_id} when attempting to log data")
            continue

        is_valid_value, value = to_float(value)
        if not is_valid_value:
            return {"error": "Invalid value"}
        try:
            unit=Unit(unit)
        except ValueError:
            logger.info(f"Unable to log sensor data because unit {unit} isn't valid")
            return {"error": f"Unable to log sensor data because unit {unit} isn't valid. Unit must be one of the following units: {[type.value for type in Unit]}"}
        try:
            sensor_data = Sensor_Data(sensor_id=sensor_id, value=value, unit=unit)
            db.session.add(sensor_data)
            readings_added.append(sensor_data)
            logger.info(f'Successfully added sensor data for sesor {sensor_id}')
        except SQLAlchemyError:
            logger.error(f"Error adding sensor data for sensor {sensor_id}")
            db.session.rollback()
            return {"error": "Error adding sensor data"}
    logger.info(f"{len(readings_added)} out of {len(data)} requested data were points added for {user_id}")
    db.session.commit()
    return [reading.to_dict() for reading in readings_added]

def get_sensor_data(user_id, sensor_id):
    try:
        sensor = Sensor.query.filter_by(id=sensor_id, user_id=user_id).first()
        if not sensor:
            return {"error": "Sensor not found", "code": 404}

        data_rows = Sensor_Data.query.filter_by(sensor_id=sensor_id).order_by(Sensor_Data.created_at.asc()).all()
        return [d.to_dict() for d in data_rows]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching sensor data for sensor {sensor_id}: {e}")
        return {"error": "Internal service error", "code": 500}

def remove_sensor_data(user_id, sensor_id, data_id):
    try:
        sensor = Sensor.query.filter_by(id=sensor_id, user_id=user_id).first()
        if not sensor:
            return {"error": "Sensor not found", "code": 404}

        deleted = Sensor_Data.query.filter_by(id=data_id).delete()
        db.session.commit()
        logger.info(f"Deleted {deleted} data rows for sensor {sensor_id}")
        if deleted:
            return {"msg": f"Successfully removed sensor data ID {data_id} for sensor {sensor_id}"}
        else:
            return {"msg": f"Data ID {data_id} for sensor {sensor_id} does not exist"}
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error deleting sensor data for sensor {sensor_id}: {e}")
        return {"error": "Internal service error", "code": 500}


def remove_all_sensor_data(user_id, sensor_id):
    try:
        sensor = Sensor.query.filter_by(id=sensor_id, user_id=user_id).first()
        if not sensor:
            return {"error": "Sensor not found", "code": 404}
        
        deleted = Sensor_Data.query.filter_by(sensor_id=sensor_id).delete()

        db.session.commit()
        logger.info(f"Deleted all data rows for sensor {sensor_id}")
        if deleted:
            return {"msg": f"Successfully removed sensor data for sensor {sensor_id}"}
        else:
            return {"msg": f"No sensor data to remove for sensor {sensor_id}"}
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error deleting sensor data for sensor {sensor_id}: {e}")
        return {"error": "Internal service error", "code": 500}