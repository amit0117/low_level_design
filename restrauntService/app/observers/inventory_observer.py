from abc import ABC, abstractmethod
from app.models.item import Item
from threading import Lock


class InventoryObserver(ABC):
    @abstractmethod
    def update_inventory_status(self, item: Item, quantity: int) -> None:
        if quantity <= 0:
            print(f"Item {item.get_name()} has been out of stock. Please restock the item.")
        else:
            print(f"Item {item.get_name()} is re-stocked. Quantity: {quantity}")


class InventorySubject:
    def __init__(self) -> None:
        self.observers: list[InventoryObserver] = []
        self.lock = Lock()

    def add_observer(self, observer: InventoryObserver) -> None:
        with self.lock:
            self.observers.append(observer)

    def remove_observer(self, observer: InventoryObserver) -> None:
        with self.lock:
            self.observers.remove(observer)

    def notify_observers(self, item: Item, quantity: int) -> None:
        for observer in self.observers:
            observer.update_inventory_status(item, quantity)
