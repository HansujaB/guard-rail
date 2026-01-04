from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class IntentAnalysis(Base):
    __tablename__ = "intent_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_segment_id = Column(UUID(as_uuid=True), ForeignKey("track_segments.id"), index=True)
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=True, index=True)
    analysis_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Final fusion model output
    final_intent_score = Column(Numeric(5, 4), nullable=False)  # 0.0 to 1.0
    risk_level = Column(String(20), nullable=False, index=True)  # low, medium, high, critical
    model_version = Column(String(50))  # ML model version used
    confidence_score = Column(Numeric(5, 4))  # Model confidence
    
    # Individual model outputs (stored as JSONB for flexibility)
    model_outputs = Column(JSONB, nullable=False)
    """
    Structure:
    {
        "vibration_autoencoder": {
            "anomaly_score": 0.85,
            "tampering_probability": 0.78,
            "confidence": 0.92
        },
        "acoustic_cnn": {
            "tool_detected": true,
            "tool_type": "drill",
            "confidence": 0.87,
            "sound_pattern": "metal_cutting"
        },
        "human_detection": {
            "human_present": true,
            "confidence": 0.94,
            "duration_minutes": 3.5,
            "activity_type": "loitering"
        },
        "lstm_sequence": {
            "sabotage_pattern_score": 0.82,
            "sequence_confidence": 0.89,
            "pattern_type": "progressive_tampering"
        },
        "weather_filter": {
            "weather_excluded": false,
            "weather_conditions": "clear",
            "false_positive_risk": 0.05
        },
        "fusion_model": {
            "final_score": 0.80,
            "contributing_factors": {
                "vibration": 0.25,
                "acoustic": 0.18,
                "human_presence": 0.20,
                "sequence_pattern": 0.22,
                "timing": 0.15
            }
        }
    }
    """
    
    # XAI Layer - Explainable AI outputs
    xai_explanation = Column(JSONB)
    """
    Structure:
    {
        "explanation": "High intent score due to combination of...",
        "signal_contributions": [
            {
                "signal": "Human presence detected",
                "contribution": 0.25,
                "confidence": 0.92
            },
            {
                "signal": "Tool-metal acoustic signature",
                "contribution": 0.18,
                "confidence": 0.87
            },
            ...
        ],
        "feature_importance": {
            "vibration_anomaly": 0.28,
            "acoustic_tool": 0.22,
            "human_presence": 0.25,
            "night_timing": 0.12,
            "train_proximity": 0.13
        },
        "reasoning_steps": [
            "Detected vibration anomaly with 85% confidence",
            "Acoustic CNN identified drill sound pattern",
            "Human presence confirmed for 3.5 minutes",
            "LSTM detected progressive tampering sequence",
            "Weather conditions clear - no false positive risk"
        ]
    }
    """
    
    explanation_text = Column(Text)  # Human-readable explanation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    track_segment = relationship("TrackSegment")
    alert = relationship("Alert")

