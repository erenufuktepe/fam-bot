from typing import Optional

from pydantic import BaseModel, Field


class BirthdayDTO(BaseModel):
    person_name: str = Field(..., description="Name of the birthday person")
    user_id: int = Field(..., description="Telegram user id")
    month: int = Field(..., description="The month of birth")
    day: int = Field(..., description="The day of birth")
