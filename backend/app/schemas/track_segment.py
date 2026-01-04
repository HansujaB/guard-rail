from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class TrackSegmentBase(BaseModel):
    segment_id: str
    name: str
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    length_km: Optional[Decimal] = None
    status: str = "normal"


class TrackSegmentCreate(TrackSegmentBase):
    division_id: Optional[UUID] = None


class TrackSegmentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    length_km: Optional[Decimal] = None
    total_sensors: Optional[int] = None
    active_sensors: Optional[int] = None


class TrackSegment(TrackSegmentBase):
    id: UUID
    division_id: Optional[UUID] = None
    total_sensors: int = 0
    active_sensors: int = 0
    last_update: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

