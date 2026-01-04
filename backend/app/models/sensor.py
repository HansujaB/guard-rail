from sqlalchemy import Column, String, DateTime, Boolean, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import uuid
from app.database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String(50), unique=True, nullable=False)
    track_segment_id = Column(UUID(as_uuid=True), ForeignKey("track_segments.id", ondelete="CASCADE"), index=True)
    sensor_type = Column(String(50), nullable=False, index=True)  # vibration, acoustic, temperature, pressure, etc.
    location = Column(Geometry('POINT'))
    installation_date = Column(Date)
    is_active = Column(Boolean, default=True, index=True)
    last_data_received = Column(DateTime(timezone=True))
    battery_level = Column(Integer)  # Percentage
    firmware_version = Column(String(50))
    calibration_data = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    track_segment = relationship("TrackSegment", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")

