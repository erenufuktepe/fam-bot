from app.model_mapper import ModelMapper
from app.models import ShoppingItem
from app.repositories import ShoppingItemRepository
from app.schemas import ShoppingItemDTO


class ShoppingItemService:
    def __init__(self, repository: ShoppingItemRepository):
        self.repository = repository

    def add(self, dto: ShoppingItemDTO) -> ShoppingItemDTO:
        try:
            item = ModelMapper.from_schema(dto, ShoppingItem)
            return self.repository.upsert(item)
        except Exception as exc:
            raise Exception(f"Error creating shopping item: {exc}") from exc

    def get_shopping_items(self) -> list[ShoppingItemDTO] | None:
        try:
            items = self.repository.get_all()
            return ModelMapper.from_model_list(items, ShoppingItemDTO)
        except Exception as exc:
            raise Exception(f"Error fetching shopping items: {exc}") from exc

    def delete(self, item_id: int) -> bool:
        try:
            item = self.repository.get_by_id(item_id)
            if not item:
                raise Exception("Item not found.")
            return self.repository.delete(item)
        except Exception as exc:
            raise Exception(f"Error removing shopping item: {exc}") from exc
