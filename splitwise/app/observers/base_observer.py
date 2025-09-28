from abc import ABC, abstractmethod
from typing import Any, Optional


class Observer(ABC):
    """Simple Observer interface"""

    @abstractmethod
    def update(self, data: Optional[Any] = None, message: Optional[str] = None) -> None:
        """Update method called when the subject notifies observers"""
        pass


class Subject(ABC):
    """Simple Subject implementation"""

    def __init__(self):
        self._observers: list[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        """Add an observer to the notification list"""
        if observer and observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the notification list"""
        if observer in self._observers:
            self._observers.remove(observer)

    @abstractmethod
    def notify_observers(self, data: Optional[Any], message: Optional[str]) -> None:
        """Notify all observers with the given data and message"""
        raise NotImplementedError("Subclasses must implement this method")
