from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.repositories.item_repository import ItemRepository

if TYPE_CHECKING:
    from app.models.library_item import LibraryItem


class ItemSearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str) -> list[LibraryItem]:
        raise NotImplementedError("Subclasses must implement this method")


class SearchByTitleStrategy(ItemSearchStrategy):
    def __init__(self):
        self.item_repository = ItemRepository.get_instance()

    def search(self, query: str) -> list[LibraryItem]:
        return sorted(self.item_repository.get_items_by_title(query), key=lambda x: x.get_title())[:5]


class SearchByAuthorStrategy(ItemSearchStrategy):
    def __init__(self):
        self.item_repository = ItemRepository.get_instance()

    def search(self, query: str) -> list[LibraryItem]:
        return sorted(self.item_repository.get_items_by_author(query), key=lambda x: x.get_author())[:5]
