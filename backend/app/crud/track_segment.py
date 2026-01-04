from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models import TrackSegment
from app.schemas.track_segment import TrackSegmentCreate, TrackSegmentUpdate


def get_track(db: Session, track_id: UUID) -> Optional[TrackSegment]:
    """Get track segment by ID"""
    return db.query(TrackSegment).filter(TrackSegment.id == track_id).first()


def get_tracks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[TrackSegment]:
    """Get list of track segments"""
    query = db.query(TrackSegment)
    if status:
        query = query.filter(TrackSegment.status == status)
    return query.offset(skip).limit(limit).all()


def create_track(db: Session, track: TrackSegmentCreate) -> TrackSegment:
    """Create a new track segment"""
    db_track = TrackSegment(**track.model_dump())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def update_track(
    db: Session,
    track_id: UUID,
    track_update: TrackSegmentUpdate
) -> Optional[TrackSegment]:
    """Update a track segment"""
    db_track = get_track(db, track_id=track_id)
    if not db_track:
        return None
    
    update_data = track_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_track, field, value)
    
    db.commit()
    db.refresh(db_track)
    return db_track


def delete_track(db: Session, track_id: UUID) -> bool:
    """Delete a track segment"""
    db_track = get_track(db, track_id=track_id)
    if not db_track:
        return False
    db.delete(db_track)
    db.commit()
    return True

