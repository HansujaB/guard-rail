from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="CASCADE"), index=True)
    reading_type = Column(String(50), nullable=False, index=True)  # vibration, acoustic, temperature, pressure
    value = Column(Numeric(12, 4), nullable=False)
    unit = Column(String(20))  # Hz, dB, °C, kPa
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    quality_score = Column(Numeric(5, 2))  # Data quality indicator (0-100)
    metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    sensor = relationship("Sensor", back_populates="readings")

