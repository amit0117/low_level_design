from typing import List
from threading import Lock
from app.models.item import Item
from app.models.inventory import Inventory


class InventoryRepository:
    """Repository for inventory data access operations - Single Responsibility: Inventory persistence"""

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
            self.inventory = Inventory()
            self.data_lock = Lock()
            self._initialized = True

    def save_item(self, item: Item, quantity: int) -> None:
        """Save item to inventory"""
        with self.data_lock:
            self.inventory.add_item(item, quantity)

    def find_item_quantity(self, item: Item) -> int:
        """Get item quantity"""
        return self.inventory.get_item_quantity(item)

    def find_available_items(self) -> List[Item]:
        """Get all available items"""
        return [item for item in self.inventory.items.keys() if self.inventory.get_item_quantity(item) > 0]

    def find_out_of_stock_items(self) -> List[Item]:
        """Get all out of stock items"""
        return [item for item in self.inventory.items.keys() if self.inventory.get_item_quantity(item) <= 0]

    def update_quantity(self, item: Item, quantity_change: int) -> None:
        """Update item quantity"""
        with self.data_lock:
            if quantity_change > 0:
                self.inventory.add_item(item, quantity_change)
            else:
                self.inventory.remove_item(item.get_name(), abs(quantity_change))

    def delete_item(self, item: Item) -> None:
        """Delete item from inventory"""
        with self.data_lock:
            if item in self.inventory.items:
                del self.inventory.items[item]
