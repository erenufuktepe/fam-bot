from sqlalchemy.orm import Session

from app.models import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    """Repository for Task model."""

    def __init__(self, session: Session):
        super().__init__(session, Task)
