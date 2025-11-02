from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("execute method must be implemented")

    @abstractmethod
    def undo(self) -> None:
        raise NotImplementedError("undo method must be implemented")
