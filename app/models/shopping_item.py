import datetime as dt

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text

from app.models.base import Base


class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(BigInteger, ForeignKey("users.id"))
    item_name = Column(String, nullable=False)
    quantity = Column(Integer)
    note = Column(Text)
    created_datetime = Column(
        DateTime(timezone=True), default=dt.datetime.now(dt.timezone.utc)
    )
