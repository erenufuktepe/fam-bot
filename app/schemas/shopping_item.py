from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    id: int = Field(None, description="Shopping item ID")
    user_id: int = Field(None, description="Telegram user id")
    item_name: str = Field(..., description="Shopping item name")
    quantity: int = Field(..., description="Shopping item quantity")
    note: str = Field(..., description="Shopping item notes")
    created_datetime: datetime = Field(
        datetime.now(ZoneInfo("America/Chicago")),
        description="Shopping item created datetime",
    )
