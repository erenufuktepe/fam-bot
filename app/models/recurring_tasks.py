from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

from app.enums import Cadence, Status

Base = declarative_base()


class RecurringTask(Base):
    __tablename__ = "recurring_tasks"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    cadence = Column(Enum(Cadence), nullable=False)
    weekday = Column(Integer)  # 0-6 when weekly
    monthday = Column(Integer)  # 1-31 when monthly
    status = Column(Enum(Status), nullable=False)
    notes = Column(String)
