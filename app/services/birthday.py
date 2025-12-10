from app.enums import Month
from app.model_mapper import ModelMapper
from app.models import Birthday
from app.repositories import BirthdayRepository
from app.schemas import BirthdayDTO
from app.utils import datetime


class BirthdayServiceExpection(Exception): ...


class BirthdayServiceIntegrityException(Exception): ...


class BirthdayService:
    def __init__(self, repository: BirthdayRepository):
        self.repository = repository

    def get_upcoming_birthdays(self) -> list[BirthdayDTO]:
        try:
            month = datetime.get_current_month()
            birthdays = self.repository.get_by_month(month)
            return ModelMapper.from_model_list(birthdays, BirthdayDTO)
        except Exception as exc:
            raise BirthdayServiceExpection(
                f"Error getting birthday for {Month.from_number(month)}: {exc}"
            ) from exc

    def add(self, dto: BirthdayDTO) -> Birthday:
        try:
            dto.person_name = dto.person_name.title()
            birthday = ModelMapper.from_schema(dto, Birthday)
            return self.repository.upsert(birthday)
        except Exception as exc:
            raise BirthdayServiceExpection(
                f"Error creating birhday information: {exc}"
            ) from exc

    def delete(self, person_name: str) -> bool:
        try:
            person_name = person_name.title()
            birthday = self.repository.get_by_id(person_name)
            if not birthday:
                raise Exception("Birthday not found.")
            return self.repository.delete(birthday)
        except Exception as exc:
            raise BirthdayServiceExpection(f"Error deleting birthday: {exc}") from exc
