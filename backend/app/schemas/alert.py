from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class AlertBase(BaseModel):
    alert_type: str
    severity: str
    message: str
    location: Optional[str] = None
    intent_score: Optional[Decimal] = None


class AlertCreate(AlertBase):
    track_segment_id: UUID
    alert_id: str
    metadata: Optional[Dict[str, Any]] = None


class AlertUpdate(BaseModel):
    status: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None


class Alert(AlertBase):
    id: UUID
    alert_id: str
    track_segment_id: UUID
    status: str
    detected_at: datetime
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[UUID] = None
    related_incident_id: Optional[UUID] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

