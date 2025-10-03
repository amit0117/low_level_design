from threading import Lock
from app.models.item import Item
from collections import defaultdict
from app.exceptions.item import MissingItemException
from app.exceptions.inventory import InsufficientStockException
from app.models.enums import MenuCategory


class Inventory:
    def __init__(self) -> None:
        # store item_name and tuple of item and quantity
        self.items: dict[Item, int] = defaultdict(int)
        self.lock = Lock()

    def add_item(self, item: Item, quantity: int) -> None:
        with self.lock:
            self.items[item] += quantity

    def get_item_quantity(self, item: Item) -> int:
        return self.items[item]

    def get_veg_items(self) -> list[Item]:
        return [item for item in self.items if item.get_category() == MenuCategory.VEG]

    def get_non_veg_items(self) -> list[Item]:
        return [item for item in self.items if item.get_category() == MenuCategory.NON_VEG]

    def remove_item(self, item_name: str, quantity: int) -> None:
        item = next((item for item in self.items if item.get_name().lower() == item_name.lower()), None)
        if not item:
            raise MissingItemException(item_name)

        with self.lock:
            if self.items[item] < quantity:
                raise InsufficientStockException(item_name, quantity, self.items[item])
            self.items[item] -= quantity
            if self.items[item] == 0:
                del self.items[item]
