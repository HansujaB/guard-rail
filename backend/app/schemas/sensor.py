from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


class SensorBase(BaseModel):
    sensor_id: str
    sensor_type: str
    is_active: bool = True
    battery_level: Optional[int] = None
    firmware_version: Optional[str] = None


class SensorCreate(SensorBase):
    track_segment_id: UUID
    installation_date: Optional[date] = None
    calibration_data: Optional[Dict[str, Any]] = None


class Sensor(SensorBase):
    id: UUID
    track_segment_id: UUID
    installation_date: Optional[date] = None
    last_data_received: Optional[datetime] = None
    calibration_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SensorReadingCreate(BaseModel):
    sensor_id: UUID
    reading_type: str
    value: Decimal
    unit: Optional[str] = None
    timestamp: datetime
    quality_score: Optional[Decimal] = None
    metadata: Optional[Dict[str, Any]] = None


class SensorReading(BaseModel):
    id: UUID
    sensor_id: UUID
    reading_type: str
    value: Decimal
    unit: Optional[str] = None
    timestamp: datetime
    quality_score: Optional[Decimal] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

