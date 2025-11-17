import datetime as dt

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base


class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    quantity = Column(Integer)
    notes = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=dt.datetime.now(dt.timezone.utc)
    )
