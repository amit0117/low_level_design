from app.models.item import Item
from threading import Lock
from app.exceptions.item import MissingItemException
from app.models.enums import MenuCategory


class Menu:
    def __init__(self) -> None:
        self.lock = Lock()
        self.items: list[Item] = []

    def add_item(self, item: Item) -> None:
        with self.lock:
            self.items.append(item)

    def get_items(self) -> list[Item]:
        return self.items

    def get_veg_items(self) -> list[Item]:
        return [item for item in self.items if item.get_category() == MenuCategory.VEG]

    def get_non_veg_items(self) -> list[Item]:
        return [item for item in self.items if item.get_category() == MenuCategory.NON_VEG]

    def remove_item(self, item: Item) -> None:
        with self.lock:
            if item not in self.items:
                raise MissingItemException(item.get_name())
            self.items.remove(item)
