from threading import Lock
from typing import Optional
from app.models.library_item import LibraryItem
from app.models.enums import ItemType


class ItemRepository:
    _lock = Lock()
    _instance: "ItemRepository" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "items"):
            return
        self.process_lock = Lock()
        self.items: list[LibraryItem] = []

    @classmethod
    def get_instance(cls) -> "ItemRepository":
        return cls._instance or cls()

    def add_item(self, item: LibraryItem):
        with self.process_lock:
            self.items.append(item)

    def remove_item(self, item: LibraryItem):
        with self.process_lock:
            if not self.get_item_by_id(item.get_id()):
                raise ValueError("Item not found")
            self.items.remove(item)

    def get_item_by_id(self, id: str) -> Optional[LibraryItem]:
        return next((item for item in self.items if item.get_id() == id), None)

    def get_item_by_title(self, title: str) -> Optional[LibraryItem]:
        return next((item for item in self.items if item.get_title() == title), None)

    def get_item_by_author(self, author: str) -> Optional[LibraryItem]:
        return next((item for item in self.items if item.get_author() == author), None)

    def get_item_by_type(self, type: ItemType) -> Optional[LibraryItem]:
        return next((item for item in self.items if item.get_type() == type), None)

    def get_items_by_title(self, title: str) -> list[LibraryItem]:
        return [item for item in self.items if item.get_title() == title]

    def get_items_by_author(self, author: str) -> list[LibraryItem]:
        return [item for item in self.items if item.get_author() == author]

    def get_items_by_type(self, type: ItemType) -> list[LibraryItem]:
        return [item for item in self.items if item.get_type() == type]

    def get_all_items(self) -> list[LibraryItem]:
        return self.items

