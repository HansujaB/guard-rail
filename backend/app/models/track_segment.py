from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import uuid
from app.database import Base


class TrackSegment(Base):
    __tablename__ = "track_segments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segment_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    division_id = Column(UUID(as_uuid=True), ForeignKey("divisions.id"))
    start_location = Column(String(255))
    end_location = Column(String(255))
    start_coordinates = Column(Geometry('POINT'))
    end_coordinates = Column(Geometry('POINT'))
    length_km = Column(Numeric(10, 2))
    status = Column(String(20), default="normal", index=True)  # normal, suspicious, danger
    total_sensors = Column(Integer, default=0)
    active_sensors = Column(Integer, default=0)
    last_update = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    division = relationship("Division", back_populates="track_segments")
    sensors = relationship("Sensor", back_populates="track_segment", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="track_segment")

