from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import TrackSegment, Alert, Sensor
from app.schemas.dashboard import DashboardOverview, SystemMetric, AlertSummary

router = APIRouter()


@router.get("/dashboard/overview", response_model=DashboardOverview)
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get dashboard overview data"""
    
    # Get track segments count
    total_tracks = db.query(TrackSegment).count()
    active_tracks = db.query(TrackSegment).filter(TrackSegment.status != "normal").count()
    
    # Get alerts count by severity
    alerts_critical = db.query(Alert).filter(Alert.severity == "critical", Alert.status == "active").count()
    alerts_warning = db.query(Alert).filter(Alert.severity == "warning", Alert.status == "active").count()
    alerts_info = db.query(Alert).filter(Alert.severity == "info", Alert.status == "active").count()
    total_alerts = alerts_critical + alerts_warning + alerts_info
    
    # Get sensors count
    active_sensors = db.query(Sensor).filter(Sensor.is_active == True).count()
    
    # System metrics (mock for now - TODO: implement real system monitoring)
    system_metrics = [
        SystemMetric(name="Sensors Online", value=active_sensors, unit="/ 856", status="healthy"),
        SystemMetric(name="Edge Nodes", value=98.7, unit="%", status="healthy"),
        SystemMetric(name="Data Pipeline", value=12.4, unit="k/s", status="healthy"),
        SystemMetric(name="Database", value=99.9, unit="% up", status="healthy"),
        SystemMetric(name="Network", value=24, unit="ms", status="healthy"),
        SystemMetric(name="Storage", value=67, unit="%", status="warning"),
    ]
    
    return DashboardOverview(
        active_threats=alerts_critical,
        track_segments=total_tracks,
        active_track_segments=active_tracks,
        running_trains=124,  # TODO: Get from trains table
        drones_active=8,  # TODO: Get from drones table
        alert_summary=AlertSummary(
            total=total_alerts,
            critical=alerts_critical,
            warning=alerts_warning,
            info=alerts_info
        ),
        system_status={"metrics": system_metrics}
    )


@router.get("/dashboard/system-status")
async def get_system_status(db: Session = Depends(get_db)):
    """Get system status metrics"""
    active_sensors = db.query(Sensor).filter(Sensor.is_active == True).count()
    
    return {
        "metrics": [
            {"name": "Sensors Online", "value": active_sensors, "unit": "/ 856", "status": "healthy"},
            {"name": "Edge Nodes", "value": 98.7, "unit": "%", "status": "healthy"},
            {"name": "Data Pipeline", "value": 12.4, "unit": "k/s", "status": "healthy"},
            {"name": "Database", "value": 99.9, "unit": "% up", "status": "healthy"},
            {"name": "Network", "value": 24, "unit": "ms", "status": "healthy"},
            {"name": "Storage", "value": 67, "unit": "%", "status": "warning"},
        ]
    }

