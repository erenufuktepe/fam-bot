from sqlalchemy import BigInteger, Boolean, Column, String

from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String)
    is_allowed = Column(Boolean, default=False)
