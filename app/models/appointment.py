from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    start_at = Column(DateTime(timezone=True), index=True, nullable=False)
    location = Column(String)
    notes = Column(String)
