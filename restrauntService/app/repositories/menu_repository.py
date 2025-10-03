from typing import List, Optional
from threading import Lock
from app.models.item import Item
from app.models.menu import Menu


class MenuRepository:
    """Repository for menu data access operations - Single Responsibility: Menu persistence"""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.menu = Menu()
            self.data_lock = Lock()
            self._initialized = True

    def save_item(self, item: Item) -> None:
        """Save menu item"""
        with self.data_lock:
            self.menu.add_item(item)

    def find_all_items(self) -> List[Item]:
        """Get all menu items"""
        return self.menu.get_items()

    def find_item_by_name(self, name: str) -> Optional[Item]:
        """Find menu item by name"""
        return next((item for item in self.menu.get_items() if item.get_name().lower() == name.lower()), None)

    def find_veg_items(self) -> List[Item]:
        """Get all vegetarian items"""
        return self.menu.get_veg_items()

    def find_non_veg_items(self) -> List[Item]:
        """Get all non-vegetarian items"""
        return self.menu.get_non_veg_items()

    def delete_item(self, item: Item) -> None:
        """Delete menu item"""
        with self.data_lock:
            self.menu.remove_item(item)
