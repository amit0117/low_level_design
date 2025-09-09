from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.stock import Stock


class StockObserver(ABC):
    @abstractmethod
    def update(self, stock: "Stock"):
        raise NotImplementedError("Update method not implemented in subclass")


class StockSubject:
    def __init__(self):
        self.observers: list[StockObserver] = []

    def add_observer(self, observer: StockObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: StockObserver):
        self.observers.remove(observer)

    def notify_observers(self, stock: "Stock"):
        for observer in self.observers:
            observer.update(stock)
