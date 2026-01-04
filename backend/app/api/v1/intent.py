from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.database import get_db
from app.schemas.ml import IntentAnalysisInput, IntentAnalysisResponse
from app.crud import intent_analysis as crud_intent
from app.services.ml_service import ml_service

router = APIRouter()


@router.post("/intent/analyze", response_model=IntentAnalysisResponse, status_code=201)
async def analyze_intent(
    input_data: IntentAnalysisInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger intent analysis using ML pipeline
    Runs all 7 ML models and returns combined result:
    1. Vibration Autoencoder - Detect physical tampering
    2. Acoustic CNN - Detect tool sounds
    3. Human Detection - Confirm human involvement
    4. LSTM Sequence Model - Detect sabotage pattern
    5. Weather Filter - Remove false positives
    6. Fusion Model - Decide intent
    7. XAI Layer - Explain decision
    """
    # Run ML pipeline
    ml_output = await ml_service.analyze_intent(input_data)
    
    # Save to database
    analysis = crud_intent.create_intent_analysis(
        db,
        track_segment_id=input_data.track_segment_id,
        alert_id=input_data.alert_id,
        ml_output=ml_output
    )
    
    return analysis


@router.get("/intent/analysis/{analysis_id}", response_model=IntentAnalysisResponse)
async def get_intent_analysis(
    analysis_id: UUID,
    db: Session = Depends(get_db)
):
    """Get intent analysis by ID"""
    analysis = crud_intent.get_intent_analysis(db, analysis_id=analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Intent analysis not found")
    return analysis


@router.get("/intent/analysis/alert/{alert_id}", response_model=IntentAnalysisResponse)
async def get_alert_intent_analysis(
    alert_id: UUID,
    db: Session = Depends(get_db)
):
    """Get intent analysis for a specific alert"""
    analysis = crud_intent.get_intent_analysis_by_alert(db, alert_id=alert_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Intent analysis not found for this alert")
    return analysis


@router.get("/intent/analysis/track/{track_id}", response_model=IntentAnalysisResponse)
async def get_track_intent_analysis(
    track_id: UUID,
    db: Session = Depends(get_db)
):
    """Get latest intent analysis for a track segment"""
    analysis = crud_intent.get_latest_intent_analysis(
        db, track_segment_id=track_id
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Intent analysis not found")
    return analysis

