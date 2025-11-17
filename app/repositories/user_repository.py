import logging

from sqlalchemy.orm import Session

from app.models.user import User

logger = logging.getLogger(__name__)


class UserRepositoryException(Exception):
    pass


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> User:
        user = self.session.query(User).filter(User.id == user_id).first()
        return user

    def add_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
