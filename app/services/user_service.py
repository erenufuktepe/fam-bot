import logging

from app.db import session_scope
from app.model_mapper import ModelMapper
from app.models.user import User as UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.user import User as UserSchema

logger = logging.getLogger(__name__)


class UserServiceException(Exception):
    pass


class UserService:
    def get_by_id(self, id: int) -> UserSchema | None:
        try:
            with session_scope() as session:
                repository = UserRepository(session)
                user = repository.get_by_id(id)
            if not user:
                logger.info(f"User with id {id} not found.")
                return None
            return ModelMapper.from_model(user, UserSchema)
        except Exception as exc:
            raise UserServiceException(f"Error getting the {id}: {exc}")

    def create_user(self, user: UserSchema) -> bool:
        try:
            with session_scope() as session:
                repository = UserRepository(session)
                if repository.get_by_id(user.id):
                    raise UserServiceException(f"User already exists.")
                _user = ModelMapper.from_schema(user, UserModel)
                repository.add_user(_user)
                return True
        except Exception as exc:
            raise UserServiceException(f"Error creating user: {exc}")


def get_user_service() -> UserService:
    return UserService()
