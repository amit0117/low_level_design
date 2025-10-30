from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import Game


class GameObserver(ABC):
    @abstractmethod
    def update(self, game: "Game") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class GameSubject:
    def __init__(self) -> None:
        self.observers: list[GameObserver] = []

    def add_observer(self, observer: GameObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: GameObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, game: "Game") -> None:
        for observer in self.observers:
            observer.update(game)
