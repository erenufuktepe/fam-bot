from typing import Optional

from sqlalchemy.orm import Session

from app.models.shopping_item import ShoppingItem


class ShoppingItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_shopping_item(self, shopping_item: ShoppingItem) -> ShoppingItem:
        self.session.add(shopping_item)
        self.session.commit()
        self.session.refresh(shopping_item)
        return shopping_item

    def clean_up_items(self) -> None:
        self.session.query(ShoppingItem).delete()
        self.session.commit()

    def get_all_items(self) -> Optional[list[ShoppingItem]]:
        items = self.session.query(ShoppingItem).all()
        return items

    def delete_by_id(self, item_id: int) -> None:
        item = (
            self.session.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
        )
        if item:
            self.session.delete(item)
            self.session.commit()
