from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., description="Telegram user id")
    name: str = Field(..., description="Telegram user name")
    is_allowed: bool = Field(..., description="Bot access")
