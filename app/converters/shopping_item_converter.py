from app.models.shopping_item import ShoppingItem as ModelShoppingItem
from app.schemas.shopping_item import ShoppingItem as SchemaShoppingItem


class ShoppingItemConverter:
    @classmethod
    def from_model(cls, model: ModelShoppingItem) -> SchemaShoppingItem:
        return SchemaShoppingItem(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            quantity=model.quantity,
            notes=model.notes,
            created_at=model.created_at,
        )

    @classmethod
    def from_schema(cls, schema: SchemaShoppingItem) -> ModelShoppingItem:
        return ModelShoppingItem(
            id=schema.id,
            user_id=schema.user_id,
            name=schema.name,
            quantity=schema.quantity,
            notes=schema.notes,
            created_at=schema.created_at,
        )

    @classmethod
    def from_model_list(
        cls, models: list[SchemaShoppingItem]
    ) -> list[SchemaShoppingItem]:
        return [cls.from_model(model) for model in models]

    @classmethod
    def from_schema_list(
        cls, schemas: list[ModelShoppingItem]
    ) -> list[ModelShoppingItem]:
        return [cls.from_schema(schema) for schema in schemas]
