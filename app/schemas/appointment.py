from datetime import datetime

from pydantic import BaseModel, Field


class AppointmentDTO(BaseModel):
    id: int = Field(None, description="Appointment ID")
    user_id: int = Field(..., description="Telegram user id")
    title: str = Field(..., description="Appointment title")
    start_datetime: datetime = Field(
        ..., description="Appointment start date and time in ISO 8601 format"
    )
    location: str | None = Field(None, description="Appointment location")
    note: str | None = Field(None, description="Appointment notes")
