from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):
    """Generic base repository offering common CRUD helpers for SQLAlchemy models."""

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def _get_primary_key_name(self) -> str:
        """Return the name of the model's primary key column."""
        mapper = inspect(self.model)
        pk_cols = mapper.primary_key

        if not pk_cols:
            raise ValueError(f"{self.model.__name__} has no primary key defined.")

        if len(pk_cols) > 1:
            raise ValueError(
                "Composite primary keys are not supported in this repository."
            )

        return pk_cols[0].name

    def get_by_id(self, id_value: any) -> T:
        """Fetch one row by primary key, no matter what the PK column is."""
        pk_name = self._get_primary_key_name()
        return (
            self.session.query(self.model)
            .filter(getattr(self.model, pk_name) == id_value)
            .first()
        )

    def upsert(self, model: T) -> T:
        """Insert or update the given model instance and return the persisted object."""
        obj = self.session.merge(model)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, model: T) -> bool:
        """Delete the given model instance from the database."""
        self.session.delete(model)
        self.session.commit()
        return True

    def get_all(self):
        """Return all objects of this model."""
        return self.session.query(self.model).all()
