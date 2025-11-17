from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    id: int = Field(None, description="Shopping item ID")
    user_id: int = Field(None, description="Telegram user id")
    name: str = Field(..., description="Shopping item name")
    quantity: int = Field(..., description="Shopping item quantity")
    notes: str = Field(..., description="Shopping item notes")
    created_at: datetime = Field(
        datetime.now(ZoneInfo("America/Chicago")),
        description="Shopping item created at",
    )
