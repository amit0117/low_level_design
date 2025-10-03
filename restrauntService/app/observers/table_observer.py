from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from threading import Lock

if TYPE_CHECKING:
    from app.models.table import Table


class TableObserver(ABC):
    def __init__(self, table: "Table") -> None:
        self.table = table

    @abstractmethod
    def update_table_status(self, table: "Table") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class TableSubject:
    def __init__(self) -> None:
        self.observers: list[TableObserver] = []
        self.lock = Lock()

    def add_observer(self, observer: TableObserver) -> None:
        with self.lock:
            self.observers.append(observer)

    def remove_observer(self, observer: TableObserver) -> None:
        with self.lock:
            self.observers.remove(observer)

    def notify_observers(self, table: "Table") -> None:
        for observer in self.observers:
            observer.update_table_status(table)
