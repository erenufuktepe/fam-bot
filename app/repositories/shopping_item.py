from sqlalchemy.orm import Session

from app.models.shopping_item import ShoppingItem
from app.repositories.base import BaseRepository


class ShoppingItemRepositoryException(Exception):
    pass


class ShoppingItemRepository(BaseRepository):
    """Repository for ShoppingItem model."""

    def __init__(self, session: Session):
        super().__init__(session, ShoppingItem)
