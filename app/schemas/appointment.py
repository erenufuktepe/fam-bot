from pydantic import BaseModel, Field


class Appointment(BaseModel):
    id: int = Field(None, description="Appointment ID")
    user_id: int = Field(None, description="Telegram user id")
    title: str = Field(..., description="Appointment title")
    start_datetime: str = Field(
        ..., description="Appointment start date and time in ISO 8601 format"
    )
    location: str = Field(..., description="Appointment location")
    note: str = Field(..., description="Appointment notes")
