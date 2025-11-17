import logging

from app.enums import Month
from app.models.birthday import Birthday as ModelBirthday
from app.schemas.birthday import Birthday as SchemaBirthday

logger = logging.getLogger(__name__)


class BirthdayConverterException(Exception):
    pass


class BirthdayConverter:
    @classmethod
    def from_model(cls, birthday: ModelBirthday) -> SchemaBirthday:
        try:
            return SchemaBirthday(
                person_name=birthday.person_name,
                month=Month.format_number(birthday.month),
                day=birthday.day,
            )
        except Exception as exc:
            raise BirthdayConverterException(
                f"Error convertering birthday to birthday schema: {exc}"
            )

    @classmethod
    def from_model_list(cls, birthdays: list[ModelBirthday]) -> list[SchemaBirthday]:
        return [cls.from_model(birthday) for birthday in birthdays]

    @classmethod
    def from_schema(cls, birthday: SchemaBirthday) -> ModelBirthday:
        try:
            return ModelBirthday(
                person_name=birthday.person_name,
                month=Month.from_string(birthday.month).number,
                day=birthday.day,
            )
        except Exception as exc:
            raise BirthdayConverterException(
                f"Error converting birthday to birthday model: {exc}"
            )
