from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Birthday(Base):
    __tablename__ = "birthdays"
    person_name = Column(String, primary_key=True, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    day = Column(Integer, nullable=False)  # 1-31
