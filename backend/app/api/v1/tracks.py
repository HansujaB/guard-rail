from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import TrackSegment
from app.schemas.track_segment import TrackSegment as TrackSegmentSchema, TrackSegmentCreate, TrackSegmentUpdate
from app.crud import track_segment as crud_track

router = APIRouter()


@router.get("/tracks", response_model=List[TrackSegmentSchema])
async def get_tracks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of track segments"""
    return crud_track.get_tracks(db, skip=skip, limit=limit, status=status)


@router.get("/tracks/{track_id}", response_model=TrackSegmentSchema)
async def get_track(track_id: UUID, db: Session = Depends(get_db)):
    """Get specific track segment by ID"""
    track = crud_track.get_track(db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track segment not found")
    return track


@router.post("/tracks", response_model=TrackSegmentSchema, status_code=201)
async def create_track(track: TrackSegmentCreate, db: Session = Depends(get_db)):
    """Create a new track segment"""
    return crud_track.create_track(db, track=track)


@router.put("/tracks/{track_id}", response_model=TrackSegmentSchema)
async def update_track(
    track_id: UUID,
    track_update: TrackSegmentUpdate,
    db: Session = Depends(get_db)
):
    """Update a track segment"""
    track = crud_track.update_track(db, track_id=track_id, track_update=track_update)
    if not track:
        raise HTTPException(status_code=404, detail="Track segment not found")
    return track


@router.get("/tracks/{track_id}/sensors")
async def get_track_sensors(track_id: UUID, db: Session = Depends(get_db)):
    """Get all sensors for a track segment"""
    track = crud_track.get_track(db, track_id=track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track segment not found")
    return track.sensors

