from app.model_mapper import ModelMapper
from app.models import User
from app.repositories import UserRepository
from app.schemas import UserDTO


class UserServiceException(Exception):
    pass


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_by_id(self, id: int) -> UserDTO | None:
        try:
            user = self.repository.get_by_id(id)
            if not user:
                return None
            return ModelMapper.from_model(user, UserDTO)
        except Exception as exc:
            raise UserServiceException(f"Error getting the {id}: {exc}") from exc

    def add(self, dto: UserDTO) -> UserDTO:
        try:
            user = ModelMapper.from_schema(dto, User)
            return self.repository.upsert(user)
        except Exception as exc:
            raise UserServiceException(f"Error creating user: {exc}")

    def is_allowed(self, id: int, username: str = None) -> bool:
        try:
            user = self.repository.get_by_id(id)

            if not user:
                user = User(id=id, username=username, is_allowed=False)
                self.repository.upsert(user)
                return False
            return user.is_allowed
        except Exception as exc:
            raise Exception(exc) from exc
