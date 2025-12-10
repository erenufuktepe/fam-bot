from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Birthday
from app.repositories.base import BaseRepository


class BirthdayRepositoryException(Exception):
    pass


class BirthdayRepository(BaseRepository):
    """Repository for Birthday model."""

    def __init__(self, session: Session):
        super().__init__(session, Birthday)

    def get_by_month(self, month: int) -> list[Birthday]:
        birthday = self.session.query(Birthday).filter(Birthday.month == month)
        return birthday.all()
