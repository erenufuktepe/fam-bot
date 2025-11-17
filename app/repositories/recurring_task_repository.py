from typing import Optional

from sqlalchemy.orm import Session

from app.enums import Status
from app.models.recurring_tasks import RecurringTask


class RecurringTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_recurring_task(self, recurring_task) -> bool:
        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        return recurring_task

    def get_recurring_tasks(
        self, weekday: int, monthday: int, status: Status
    ) -> Optional[list[RecurringTask]]:
        recurring_tasks = (
            self.session.query(RecurringTask)
            .filter(
                RecurringTask.weekday == weekday,
                RecurringTask.monthday == monthday,
                RecurringTask.status == status.value,
            )
            .all()
        )
        return recurring_tasks

    def upsert_recurring_task(self, recurring_task: RecurringTask) -> RecurringTask:
        self.session.merge(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        return recurring_task
