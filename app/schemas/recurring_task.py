from typing import Optional

from pydantic import BaseModel, Field


class RecurringTask(BaseModel):
    user_id: int = Field(..., description="Telegram user id")
    title: str = Field(..., description="Recurring task title")
    cadence: str = Field(..., description="Recurring task cadence")
    weekday: Optional[int] = Field(None, description="0-6 when weekly")
    monthday: Optional[int] = Field(None, description="1-31 when monthly")
    status: str = Field(..., description="Recurring task status")
    notes: Optional[str] = Field(None, description="Recurring task notes")
