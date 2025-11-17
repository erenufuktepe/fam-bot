from app.converters.recurring_task_converter import RecurringTaskConverter
from app.db import session_scope
from app.repositories.recurring_task_repository import RecurringTaskRepository
from app.schemas.recurring_task import RecurringTask


class RecurringTaskService:
    def __init__(self):
        self.converter = RecurringTaskConverter()

    def add_recurring_task(self, task: RecurringTask):
        try:
            with session_scope() as session:
                repository = RecurringTaskRepository(session)
                _task = self.converter.from_schema(task)
                return repository.add_recurring_task(_task)
        except Exception as exc:
            raise Exception(f"Error creating recurring task: {exc}")


def get_recurring_task_service() -> RecurringTaskService:
    return RecurringTaskService()
