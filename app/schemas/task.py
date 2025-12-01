from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(None, description="Task ID")
    user_id: int = Field(..., description="Telegram user id")
    chat_id: int = Field(..., description="Telegram chat id")
    task_name: str = Field(..., description="Recurring task title")
    cron_expression: str = Field(..., description="Recurring task cadence")
    status: str = Field(..., description="Recurring task status")
    note: Optional[str] = Field(None, description="Recurring task notes")
