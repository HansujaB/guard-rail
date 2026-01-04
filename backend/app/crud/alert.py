from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models import Alert
from app.schemas.alert import AlertCreate, AlertUpdate


def get_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
    """Get alert by ID"""
    return db.query(Alert).filter(Alert.id == alert_id).first()


def get_alerts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    track_segment_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Alert]:
    """Get list of alerts with filters"""
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    if track_segment_id:
        query = query.filter(Alert.track_segment_id == track_segment_id)
    if start_date:
        query = query.filter(Alert.detected_at >= start_date)
    if end_date:
        query = query.filter(Alert.detected_at <= end_date)
    
    return query.order_by(Alert.detected_at.desc()).offset(skip).limit(limit).all()


def create_alert(db: Session, alert: AlertCreate) -> Alert:
    """Create a new alert"""
    db_alert = Alert(
        **alert.model_dump(),
        detected_at=datetime.utcnow()
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def update_alert(
    db: Session,
    alert_id: UUID,
    alert_update: AlertUpdate
) -> Optional[Alert]:
    """Update an alert"""
    db_alert = get_alert(db, alert_id=alert_id)
    if not db_alert:
        return None
    
    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert


def acknowledge_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
    """Acknowledge an alert"""
    db_alert = get_alert(db, alert_id=alert_id)
    if not db_alert:
        return None
    
    db_alert.status = "acknowledged"
    db_alert.acknowledged_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert


def resolve_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
    """Resolve an alert"""
    db_alert = get_alert(db, alert_id=alert_id)
    if not db_alert:
        return None
    
    db_alert.status = "resolved"
    db_alert.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert

