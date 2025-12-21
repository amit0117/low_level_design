from abc import ABC, abstractmethod


class InventoryObserver(ABC):
    @abstractmethod
    def update_inventory_status(self, item: str, quantity: int) -> None:
        raise NotImplementedError("Subclass must implement this method")
