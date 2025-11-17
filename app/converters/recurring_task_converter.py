from app.models.recurring_tasks import RecurringTask as RecurringTaskModel
from app.schemas.recurring_task import RecurringTask as RecurringTaskSchema


class RecurringTaskConverter:
    @classmethod
    def from_model(cls, task: RecurringTaskModel) -> RecurringTaskSchema:
        try:
            return RecurringTaskSchema(
                id=task.id,
                name=task.name,
                interval_days=task.interval_days,
                last_completed=task.last_completed,
            )
        except Exception as exc:
            raise Exception(f"Error converting recurring task to schema: {exc}")

    @classmethod
    def from_schema(cls, task: RecurringTaskSchema) -> RecurringTaskModel:
        try:
            return RecurringTaskModel(
                id=task.id,
                name=task.name,
                interval_days=task.interval_days,
                last_completed=task.last_completed,
            )
        except Exception as exc:
            raise Exception(f"Error converting recurring task to model: {exc}")

    @classmethod
    def from_model_list(
        cls, tasks: list[RecurringTaskModel]
    ) -> list[RecurringTaskSchema]:
        return [cls.from_model(task) for task in tasks]

    @classmethod
    def from_schema_list(
        cls, tasks: list[RecurringTaskSchema]
    ) -> list[RecurringTaskModel]:
        return [cls.from_schema(task) for task in tasks]
