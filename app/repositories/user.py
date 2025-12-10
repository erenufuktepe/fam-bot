from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepositoryException(Exception):
    pass


class UserRepository(BaseRepository):
    """Repository for User model."""

    def __init__(self, session: Session):
        super().__init__(session, User)
