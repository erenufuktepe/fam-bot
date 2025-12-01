from app.db import session_scope
from app.model_mapper import ModelMapper
from app.repositories.task_repository import TaskRepository
from app.schemas.task import Task


class TaskService:
    def __init__(self):
        pass

    def add_recurring_task(self, task: Task):
        try:
            with session_scope() as session:
                repository = TaskRepository(session)
                _task = ModelMapper.from_schema(task, Task)
                return repository.add_recurring_task(_task)
        except Exception as exc:
            raise Exception(f"Error creating recurring task: {exc}")


def get_recurring_task_service() -> TaskService:
    return TaskService()
