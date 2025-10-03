from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from threading import Lock

if TYPE_CHECKING:
    from app.models.order import Order


class OrderObserver(ABC):
    @abstractmethod
    def update_order_status(self, order: "Order") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class OrderSubject:
    def __init__(self) -> None:
        self.observers: list[OrderObserver] = []
        self.lock = Lock()

    def add_observer(self, observer: OrderObserver) -> None:
        with self.lock:
            self.observers.append(observer)

    def remove_observer(self, observer: OrderObserver) -> None:
        with self.lock:
            self.observers.remove(observer)

    def notify_observers(self, order: "Order") -> None:
        for observer in self.observers:
            observer.update_order_status(order)
