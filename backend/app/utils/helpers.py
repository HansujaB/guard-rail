"""Utility helper functions"""

from datetime import datetime
from typing import Any


def generate_alert_id(counter: int) -> str:
    """Generate alert ID in format ALT-XXX"""
    return f"ALT-{str(counter).zfill(3)}"


def generate_incident_id(counter: int) -> str:
    """Generate incident ID"""
    return f"INC-{str(counter).zfill(3)}"

