from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class MLModelOutput(BaseModel):
    """Base schema for individual ML model outputs"""
    confidence: Decimal
    metadata: Optional[Dict[str, Any]] = None


class VibrationAutoencoderOutput(MLModelOutput):
    """Vibration Autoencoder model output"""
    anomaly_score: Decimal  # 0.0 to 1.0
    tampering_probability: Decimal
    reconstruction_error: Optional[Decimal] = None


class AcousticCNNOutput(MLModelOutput):
    """Acoustic CNN model output"""
    tool_detected: bool
    tool_type: Optional[str] = None  # drill, hammer, saw, etc.
    sound_pattern: Optional[str] = None
    spectral_features: Optional[Dict[str, Any]] = None


class HumanDetectionOutput(MLModelOutput):
    """Human Detection model output"""
    human_present: bool
    duration_minutes: Optional[Decimal] = None
    activity_type: Optional[str] = None  # loitering, crossing, maintenance, etc.
    bounding_boxes: Optional[List[Dict[str, Any]]] = None  # For camera-based detection


class LSTMSequenceOutput(MLModelOutput):
    """LSTM Sequence Model output"""
    sabotage_pattern_score: Decimal
    pattern_type: Optional[str] = None  # progressive_tampering, etc.
    sequence_confidence: Decimal


class WeatherFilterOutput(BaseModel):
    """Weather Filter output"""
    weather_excluded: bool
    weather_conditions: str
    false_positive_risk: Decimal  # 0.0 to 1.0


class FusionModelOutput(BaseModel):
    """Fusion Model output"""
    final_score: Decimal  # 0.0 to 1.0
    contributing_factors: Dict[str, Decimal]  # Contribution of each signal
    fusion_method: Optional[str] = None


class XAIExplanation(BaseModel):
    """XAI Layer output"""
    explanation: str  # Human-readable explanation
    signal_contributions: List[Dict[str, Any]]
    feature_importance: Dict[str, Decimal]
    reasoning_steps: List[str]


class IntentAnalysisInput(BaseModel):
    """Input schema for ML inference"""
    track_segment_id: UUID
    alert_id: Optional[UUID] = None
    sensor_readings: Dict[str, Any]  # Sensor data for analysis
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class IntentAnalysisOutput(BaseModel):
    """Complete ML pipeline output"""
    final_intent_score: Decimal
    risk_level: str  # low, medium, high, critical
    confidence_score: Decimal
    
    # Individual model outputs
    vibration_autoencoder: VibrationAutoencoderOutput
    acoustic_cnn: AcousticCNNOutput
    human_detection: HumanDetectionOutput
    lstm_sequence: LSTMSequenceOutput
    weather_filter: WeatherFilterOutput
    fusion_model: FusionModelOutput
    xai_explanation: XAIExplanation


class IntentAnalysisResponse(BaseModel):
    """API response schema for intent analysis"""
    id: UUID
    track_segment_id: UUID
    alert_id: Optional[UUID]
    analysis_timestamp: datetime
    final_intent_score: Decimal
    risk_level: str
    confidence_score: Optional[Decimal]
    model_outputs: Dict[str, Any]
    xai_explanation: Optional[Dict[str, Any]]
    explanation_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

