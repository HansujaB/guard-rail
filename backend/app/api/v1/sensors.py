from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.database import get_db
from app.schemas.sensor import Sensor as SensorSchema, SensorCreate, SensorReading, SensorReadingCreate
from app.crud import sensor as crud_sensor

router = APIRouter()


@router.get("/sensors", response_model=List[SensorSchema])
async def get_sensors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    track_segment_id: Optional[UUID] = None,
    sensor_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of sensors"""
    return crud_sensor.get_sensors(
        db, skip=skip, limit=limit,
        track_segment_id=track_segment_id,
        sensor_type=sensor_type
    )


@router.get("/sensors/{sensor_id}", response_model=SensorSchema)
async def get_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    """Get sensor by ID"""
    sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.post("/sensors", response_model=SensorSchema, status_code=201)
async def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """Create a new sensor"""
    return crud_sensor.create_sensor(db, sensor=sensor)


@router.get("/sensors/{sensor_id}/readings", response_model=List[SensorReading])
async def get_sensor_readings(
    sensor_id: UUID,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get sensor readings"""
    sensor = crud_sensor.get_sensor(db, sensor_id=sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return crud_sensor.get_sensor_readings(
        db, sensor_id=sensor_id,
        start_time=start_time,
        end_time=end_time,
        limit=limit
    )


@router.post("/sensors/readings", response_model=SensorReading, status_code=201)
async def create_sensor_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db)
):
    """Ingest sensor data (from IoT devices)"""
    return crud_sensor.create_sensor_reading(db, reading=reading)

