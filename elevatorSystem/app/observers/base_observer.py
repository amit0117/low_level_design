from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    @abstractmethod
    def update(self, *args: Any, **kwargs: dict) -> None:
        raise NotImplementedError("Subclasses must implement this method")
