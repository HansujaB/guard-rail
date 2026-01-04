from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(String(50), unique=True, nullable=False, index=True)
    track_segment_id = Column(UUID(as_uuid=True), ForeignKey("track_segments.id"), index=True)
    incident_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True))
    resolution_status = Column(String(50))  # resolved, under_investigation, closed
    assigned_to = Column(UUID(as_uuid=True), nullable=True)  # TODO: Add ForeignKey("users.id") when User model is created
    resolution_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

