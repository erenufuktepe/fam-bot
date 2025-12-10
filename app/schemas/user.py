from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    id: int = Field(..., description="Telegram user id")
    username: str = Field(..., description="Telegram username")
    is_allowed: bool = Field(..., description="Bot access")
