from typing import Any
from app.observers.base_observer import Observer


class BaseSubject:
    def __init__(self):
        self.observers: list[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self, *args: Any, **kwargs: dict) -> None:
        for observer in self.observers:
            observer.update(*args, **kwargs)
