from sqlalchemy import Column, String, DateTime, Boolean, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(String(50), unique=True, nullable=False, index=True)
    track_segment_id = Column(UUID(as_uuid=True), ForeignKey("track_segments.id"), index=True)
    alert_type = Column(String(50), nullable=False)  # intrusion, tampering, anomaly, surveillance
    severity = Column(String(20), nullable=False, index=True)  # critical, warning, info
    message = Column(Text, nullable=False)
    location = Column(String(255))
    intent_score = Column(Numeric(5, 4))  # 0.0 to 1.0
    status = Column(String(20), default="active", index=True)  # active, acknowledged, resolved, false_positive
    detected_at = Column(DateTime(timezone=True), nullable=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True))
    acknowledged_by = Column(UUID(as_uuid=True), nullable=True)  # TODO: Add ForeignKey("users.id") when User model is created
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(UUID(as_uuid=True), nullable=True)  # TODO: Add ForeignKey("users.id") when User model is created
    related_incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id"))
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    track_segment = relationship("TrackSegment", back_populates="alerts")

