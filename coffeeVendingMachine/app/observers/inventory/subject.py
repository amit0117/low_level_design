from app.observers.inventory.observer import InventoryObserver


class InventorySubject:
    def __init__(self):
        self.observers: list[InventoryObserver] = []

    def add_observer(self, observer: InventoryObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: InventoryObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, item: str, quantity: int) -> None:
        for observer in self.observers:
            observer.update_inventory_status(item, quantity)
