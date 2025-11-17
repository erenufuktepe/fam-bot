from sqlalchemy.orm import Session

from app.models import Birthday


class BirthdayRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_month(self, month: int) -> list[Birthday]:
        birthday = self.session.query(Birthday).filter(Birthday.month == month)
        return birthday.all()

    def add_birthday(self, birthday: Birthday) -> bool:
        self.session.add(birthday)
        self.session.commit()
        self.session.refresh(birthday)
        return birthday
