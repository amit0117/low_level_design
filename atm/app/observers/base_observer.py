from abc import ABC, abstractmethod


class BaseObserver(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        raise NotImplementedError("update method has not been implemented")
