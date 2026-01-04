from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models import Sensor, SensorReading
from app.schemas.sensor import SensorCreate, SensorReadingCreate


def get_sensor(db: Session, sensor_id: UUID) -> Optional[Sensor]:
    """Get sensor by ID"""
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    track_segment_id: Optional[UUID] = None,
    sensor_type: Optional[str] = None
) -> List[Sensor]:
    """Get list of sensors"""
    query = db.query(Sensor)
    if track_segment_id:
        query = query.filter(Sensor.track_segment_id == track_segment_id)
    if sensor_type:
        query = query.filter(Sensor.sensor_type == sensor_type)
    return query.offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: SensorCreate) -> Sensor:
    """Create a new sensor"""
    db_sensor = Sensor(**sensor.model_dump())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor_readings(
    db: Session,
    sensor_id: UUID,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100
) -> List[SensorReading]:
    """Get sensor readings"""
    query = db.query(SensorReading).filter(SensorReading.sensor_id == sensor_id)
    if start_time:
        query = query.filter(SensorReading.timestamp >= start_time)
    if end_time:
        query = query.filter(SensorReading.timestamp <= end_time)
    return query.order_by(SensorReading.timestamp.desc()).limit(limit).all()


def create_sensor_reading(db: Session, reading: SensorReadingCreate) -> SensorReading:
    """Create a new sensor reading"""
    db_reading = SensorReading(**reading.model_dump())
    db.add(db_reading)
    
    # Update sensor's last_data_received
    sensor = get_sensor(db, reading.sensor_id)
    if sensor:
        sensor.last_data_received = reading.timestamp
    
    db.commit()
    db.refresh(db_reading)
    return db_reading

