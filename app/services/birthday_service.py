import logging

from sqlalchemy.exc import IntegrityError

from app.converters.birthday_converter import BirthdayConverter
from app.db import session_scope
from app.enums import Month
from app.repositories.birthday_repository import BirthdayRepository
from app.schemas.birthday import Birthday


class BirthdayServiceExpection(Exception): ...


class BirthdayServiceIntegrityException(Exception): ...


class BirthdayService:

    def __init__(self):
        self.converter = BirthdayConverter()

    def get_birthday_by_month(self, month: int) -> list[Birthday]:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                birthdays = repository.get_by_month(month)
                return self.converter.from_model_list(birthdays)
        except Exception as exc:
            raise BirthdayServiceExpection(
                f"Error getting birthday for {Month.from_number(month)}: {exc}"
            )

    def add_birthday(self, birthday: Birthday) -> bool:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                _birthday = self.converter.from_schema(birthday)
                return repository.add_birthday(_birthday)
        except IntegrityError as exc:
            raise BirthdayServiceIntegrityException(
                "Birthday already exists in the database."
            )
        except Exception as exc:
            raise BirthdayServiceExpection(f"Error creating birhday information: {exc}")


def get_birthday_service() -> BirthdayService:
    return BirthdayService()
