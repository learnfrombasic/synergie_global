from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    """Schema for creating a new appointment."""

    name: str
    address: str
    phone: str
    email: str
    service_request: str
    preferred_date: str
    preferred_time: str


class Appointment(AppointmentCreate):
    """Schema for an existing appointment."""

    id: str
    created_at: datetime
    status: str = "scheduled"
    confirmation_id: Optional[str] = None
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    """Schema for updating an existing appointment."""

    status: Optional[str] = None
    notes: Optional[str] = None
    confirmation_id: Optional[str] = None
