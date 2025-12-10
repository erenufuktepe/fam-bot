from app.model_mapper import ModelMapper
from app.models import Task
from app.repositories import TaskRepository
from app.schemas import TaskDTO


class TaskService:
    def __init__(self, repeository: TaskRepository):
        self.repository = repeository

    def add(self, dto: TaskDTO) -> TaskDTO:
        try:
            task = ModelMapper.from_schema(dto, Task)
            return self.repository.upsert(task)
        except Exception as exc:
            raise Exception(f"Error creating recurring task: {exc}") from exc

    def delete(self, task_id: int) -> bool:
        try:
            task = self.repository.get_by_id(task_id)
            if not task:
                raise Exception("Task not found.")
            return self.repository.delete(task)
        except Exception as exc:
            raise Exception(exc) from exc
