from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.database import get_db
from app.schemas.alert import Alert as AlertSchema, AlertCreate, AlertUpdate
from app.crud import alert as crud_alert

router = APIRouter()


@router.get("/alerts", response_model=List[AlertSchema])
async def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    track_segment_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get list of alerts with filters"""
    return crud_alert.get_alerts(
        db,
        skip=skip,
        limit=limit,
        severity=severity,
        status=status,
        track_segment_id=track_segment_id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/alerts/{alert_id}", response_model=AlertSchema)
async def get_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Get alert by ID"""
    alert = crud_alert.get_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/alerts", response_model=AlertSchema, status_code=201)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert"""
    return crud_alert.create_alert(db, alert=alert)


@router.put("/alerts/{alert_id}", response_model=AlertSchema)
async def update_alert(
    alert_id: UUID,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert"""
    alert = crud_alert.update_alert(db, alert_id=alert_id, alert_update=alert_update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/alerts/{alert_id}/acknowledge", response_model=AlertSchema)
async def acknowledge_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Acknowledge an alert"""
    alert = crud_alert.acknowledge_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/alerts/{alert_id}/resolve", response_model=AlertSchema)
async def resolve_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Resolve an alert"""
    alert = crud_alert.resolve_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

