from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.message import Message


class MessageObserver(ABC):
    @abstractmethod
    def receive(self, message: "Message") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class MessageSubject:
    def __init__(self):
        self.observers: list[MessageObserver] = []

    def subscribe(self, observer: MessageObserver) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: MessageObserver) -> None:
        self.observers.remove(observer)

    def notify(self, message: "Message") -> None:
        for observer in self.observers:
            observer.receive(message)
