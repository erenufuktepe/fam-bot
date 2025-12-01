import logging

from sqlalchemy.exc import IntegrityError

from app.db import session_scope
from app.enums import Month
from app.model_mapper import ModelMapper
from app.repositories.birthday_repository import BirthdayRepository
from app.schemas.birthday import Birthday


class BirthdayServiceExpection(Exception): ...


class BirthdayServiceIntegrityException(Exception): ...


class BirthdayService:

    def __init__(self):
        pass

    def get_birthday_by_month(self, month: int) -> list[Birthday]:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                birthdays = repository.get_by_month(month)
                return ModelMapper.from_model_list(birthdays, Birthday)
        except Exception as exc:
            raise BirthdayServiceExpection(
                f"Error getting birthday for {Month.from_number(month)}: {exc}"
            )

    def add_birthday(self, birthday: Birthday) -> bool:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                _birthday = ModelMapper.from_schema(birthday, Birthday)
                return repository.add_birthday(_birthday)
        except IntegrityError as exc:
            raise BirthdayServiceIntegrityException(
                "Birthday already exists in the database."
            )
        except Exception as exc:
            raise BirthdayServiceExpection(f"Error creating birhday information: {exc}")


def get_birthday_service() -> BirthdayService:
    return BirthdayService()
