from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Birthday


class BirthdayRepositoryException(Exception):
    pass


class BirthdayRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_month(self, month: int) -> list[Birthday]:
        birthday = self.session.query(Birthday).filter(Birthday.month == month)
        return birthday.all()

    def get_by_name(self, person_name) -> Birthday:
        birthday = self.session.query(Birthday).filter(
            func.lower(Birthday.person_name) == person_name
        )
        return birthday.first()

    def add(self, birthday: Birthday) -> bool:
        self.session.add(birthday)
        self.session.commit()
        return True

    def delete(self, person_name: str) -> bool:
        birthday = self.get_by_name(person_name)
        if not birthday:
            return False
        self.session.delete(birthday)
        self.session.commit()
        return True
