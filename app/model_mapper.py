from typing import Type, TypeVar

from pydantic import BaseModel

from app.models.base import Base

T = TypeVar("T", bound=Base)
S = TypeVar("S", bound=BaseModel)


class ModelMapperException(Exception):
    pass


class ModelMapper:

    @classmethod
    def from_schema(cls, schema_obj: S, model_class: Type[T]) -> T:
        try:
            data = schema_obj.model_dump()
            fields = {col.name for col in model_class.__table__.columns}
            filtered = {k: v for k, v in data.items() if k in fields}
            return model_class(**filtered)
        except Exception as exc:
            raise ModelMapperException(f"Error converting schema to model: {exc}")

    @classmethod
    def from_model(cls, model_obj: T, schema_class: Type[S]) -> S:
        try:
            data = {
                attr: getattr(model_obj, attr)
                for attr in model_obj.__table__.columns.keys()
            }
            return schema_class(**data)
        except Exception as exc:
            raise ModelMapperException(f"Error converting model to schema: {exc}")

    @classmethod
    def from_model_list(cls, model_list: list[T], schema_class: Type[S]) -> list[S]:
        try:
            return [cls.from_model(model, schema_class) for model in model_list]
        except Exception as exc:
            raise ModelMapperException(
                f"Error converting model list to schema list: {exc}"
            )

    @classmethod
    def from_schema_list(cls, schema_list: list[S], model_class: Type[T]) -> list[T]:
        try:
            return [cls.from_schema(schema, model_class) for schema in schema_list]
        except Exception as exc:
            raise ModelMapperException(
                f"Error converting schema list to model list: {exc}"
            )
