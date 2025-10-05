from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from app.models.library_item import LibraryItem


class ItemObserver(ABC):
    @abstractmethod
    def update(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")


class ItemSubject:
    def __init__(self):
        self.observers: list[ItemObserver] = []

    def add_observer(self, observer: ItemObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: ItemObserver):
        self.observers.remove(observer)

    def notify_observers(self, item: "LibraryItem"):
        for observer in self.observers:
            observer.update(item)
