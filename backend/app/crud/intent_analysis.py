from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.intent_analysis import IntentAnalysis
from app.schemas.ml import IntentAnalysisOutput


def create_intent_analysis(
    db: Session,
    track_segment_id: UUID,
    alert_id: Optional[UUID],
    ml_output: IntentAnalysisOutput
) -> IntentAnalysis:
    """Create intent analysis record from ML output"""
    
    # Prepare model_outputs JSONB
    model_outputs = {
        "vibration_autoencoder": ml_output.vibration_autoencoder.model_dump(),
        "acoustic_cnn": ml_output.acoustic_cnn.model_dump(),
        "human_detection": ml_output.human_detection.model_dump(),
        "lstm_sequence": ml_output.lstm_sequence.model_dump(),
        "weather_filter": ml_output.weather_filter.model_dump(),
        "fusion_model": ml_output.fusion_model.model_dump(),
    }
    
    # Prepare XAI explanation JSONB
    xai_explanation = ml_output.xai_explanation.model_dump()
    
    db_analysis = IntentAnalysis(
        track_segment_id=track_segment_id,
        alert_id=alert_id,
        analysis_timestamp=datetime.utcnow(),
        final_intent_score=ml_output.final_intent_score,
        risk_level=ml_output.risk_level,
        confidence_score=ml_output.confidence_score,
        model_outputs=model_outputs,
        xai_explanation=xai_explanation,
        explanation_text=ml_output.xai_explanation.explanation,
        model_version="1.0.0"  # TODO: Get from config
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def get_intent_analysis(db: Session, analysis_id: UUID) -> Optional[IntentAnalysis]:
    """Get intent analysis by ID"""
    return db.query(IntentAnalysis).filter(IntentAnalysis.id == analysis_id).first()


def get_intent_analysis_by_alert(
    db: Session,
    alert_id: UUID
) -> Optional[IntentAnalysis]:
    """Get intent analysis for an alert"""
    return db.query(IntentAnalysis).filter(
        IntentAnalysis.alert_id == alert_id
    ).order_by(IntentAnalysis.analysis_timestamp.desc()).first()


def get_latest_intent_analysis(
    db: Session,
    track_segment_id: UUID
) -> Optional[IntentAnalysis]:
    """Get latest intent analysis for a track segment"""
    return db.query(IntentAnalysis).filter(
        IntentAnalysis.track_segment_id == track_segment_id
    ).order_by(IntentAnalysis.analysis_timestamp.desc()).first()

