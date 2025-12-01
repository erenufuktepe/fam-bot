from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text

from app.models.base import Base


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(BigInteger, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    start_datetime = Column(DateTime(timezone=True), index=True, nullable=False)
    location = Column(String)
    note = Column(Text)
