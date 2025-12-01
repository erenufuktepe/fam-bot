from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(schema="fambot")


class Base(DeclarativeBase):
    metadata = metadata
