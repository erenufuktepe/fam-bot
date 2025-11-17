from typing import Optional

from pydantic import BaseModel, Field


class Birthday(BaseModel):
    person_name: str = Field(..., description="Name of the birthday person")
    month: str = Field(..., description="The month of birth")
    day: int = Field(..., description="The day of birth")
