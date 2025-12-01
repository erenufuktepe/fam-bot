from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.db import session_scope
from app.model_mapper import ModelMapper
from app.repositories.shopping_item_repository import ShoppingItemRepository
from app.schemas.shopping_item import ShoppingItem
from app.utils import CLIParser

MAPPING = {"-i": "name", "-q": "quantity", "-n": "notes"}


class ShoppingItemService:
    def __init__(self):
        self.parser = CLIParser(
            mapping=MAPPING,
            cls=ShoppingItem,
        )

    def add_shopping_item(self, user_id: int, tokens: list) -> str:
        try:
            with session_scope() as session:
                repository = ShoppingItemRepository(session)
                item = self.parser.parse(tokens)
                item.user_id = user_id
                _item = ModelMapper.from_schema(item, ShoppingItem)
                return self._present_added_item(repository.add_shopping_item(_item))
        except Exception as exc:
            raise Exception(f"Error creating shopping item: {exc}")

    def get_shopping_items(self):
        try:
            with session_scope() as session:
                repository = ShoppingItemRepository(session)
                models = repository.get_all_items()
                return self._present_shopping_items(
                    ModelMapper.from_model_list(models, ShoppingItem)
                )
        except Exception as exc:
            raise Exception(f"Error fetching shopping items: {exc}")

    def remove_shopping_item(self, item_id: int):
        try:
            with session_scope() as session:
                repository = ShoppingItemRepository(session)
                repository.delete_by_id(item_id)
        except Exception as exc:
            raise Exception(f"Error removing shopping item: {exc}")

    def _present_added_item(self, item: ShoppingItem) -> str:
        try:
            return f"Shopping item added: {item.name.title()} 🛒"
        except Exception as exc:
            raise Exception(f"Error presenting added shopping item: {exc}")

    def _present_shopping_items(self, items: list[ShoppingItem]) -> str:
        try:
            if not items:
                return "No shopping items found. 🛒", None
            response = "<b>Shopping List:</b>\n"
            keyboard = []
            for item in items:
                response += f"\n🛒 {item.name.title()} - Quantity: {item.quantity}"
                if item.notes:
                    response += f" \n(Notes: {item.notes})\n"
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=f"{item.name.title()} - {item.quantity}",
                            callback_data=f"shop:{item.id}",
                        )
                    ]
                )
            return response, InlineKeyboardMarkup(keyboard)
        except Exception as exc:
            raise Exception(f"Error presenting shopping items: {exc}")


def get_shopping_item_service() -> ShoppingItemService:
    return ShoppingItemService()
