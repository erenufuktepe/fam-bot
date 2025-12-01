from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base

from app.enums import Cadence, Status

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(BigInteger, ForeignKey("users.id"))
    chat_id = Column(BigInteger, nullable=False)
    task_name = Column(String, nullable=False)
    cron_expression = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    notes = Column(Text)
