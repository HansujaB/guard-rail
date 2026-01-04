from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class MetricCard(BaseModel):
    label: str
    value: int | float
    unit: Optional[str] = None
    status: Optional[str] = None
    trend: Optional[str] = None
    trendValue: Optional[str] = None


class SystemMetric(BaseModel):
    name: str
    value: float
    unit: str
    status: str  # healthy, warning, critical


class SystemStatus(BaseModel):
    metrics: List[SystemMetric]


class AlertSummary(BaseModel):
    total: int
    critical: int
    warning: int
    info: int


class DashboardOverview(BaseModel):
    active_threats: int
    track_segments: int
    active_track_segments: int
    running_trains: int
    drones_active: int
    alert_summary: AlertSummary
    system_status: SystemStatus

