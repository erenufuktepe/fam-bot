import logging

from app.models.user import User as ModelUser
from app.schemas.user import User as SchemaUser

logger = logging.getLogger(__name__)


class UserConverterException(Exception):
    pass


class UserConverter:
    @staticmethod
    def from_model(user: ModelUser) -> SchemaUser:
        try:
            return SchemaUser(id=user.id, name=user.name, is_allowed=user.is_allowed)
        except Exception as exc:
            raise UserConverterException(
                f"Error convertering user to user schema: {exc}"
            )

    @staticmethod
    def from_schema(user: SchemaUser) -> ModelUser:
        try:
            return ModelUser(id=user.id, name=user.name, is_allowed=user.is_allowed)
        except Exception as exc:
            raise UserConverterException(f"Error converting user to user model: {exc}")
