from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    is_allowed = Column(Boolean, default=False)
