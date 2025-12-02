import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.db import session_scope
from app.enums import Month
from app.model_mapper import ModelMapper
from app.models.birthday import Birthday as BirthdayModel
from app.repositories.birthday_repository import BirthdayRepository
from app.schemas.birthday import Birthday as BirthdaySchema


class BirthdayServiceExpection(Exception): ...


class BirthdayServiceIntegrityException(Exception): ...


class BirthdayService:

    def __init__(self):
        pass

    async def get_upcoming_birthdays(self) -> list[BirthdaySchema]:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                month = datetime.now().month
                birthdays = repository.get_by_month(month)
                return ModelMapper.from_model_list(birthdays, BirthdaySchema)
        except Exception as exc:
            raise BirthdayServiceExpection(
                f"Error getting birthday for {Month.from_number(month)}: {exc}"
            )

    async def add_birthday(self, user_id: int, person_name: str, date: str) -> bool:
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                month, day = self._parse_date(date)
                birthday = BirthdaySchema(
                    user_id=user_id,
                    person_name=person_name,
                    month=month,
                    day=day,
                )
                _birthday = ModelMapper.from_schema(birthday, BirthdayModel)
                return repository.add(_birthday)
        except Exception as exc:
            raise BirthdayServiceExpection(f"Error creating birhday information: {exc}")

    async def delete_birthday(self, person_name: str):
        try:
            with session_scope() as session:
                repository = BirthdayRepository(session)
                repository.delete(person_name.lower())
        except Exception as exc:
            raise BirthdayServiceExpection(f"Error deleting birthday: {exc}")

    def _parse_date(self, date_str: str) -> tuple[int, int]:
        try:
            date = date_str.split("/")
            if len(date) != 2:
                raise ValueError("Date must be in MM/DD format")
            month = int(date[0])
            day = int(date[1])
            return month, day
        except ValueError as exc:
            raise BirthdayServiceExpection(f"Invalid date format: {exc}")


def get_birthday_service() -> BirthdayService:
    return BirthdayService()
