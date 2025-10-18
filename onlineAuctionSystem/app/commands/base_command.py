from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("execute method has not been implemented")

    @abstractmethod
    def undo(self):
        raise NotImplementedError("undo method has not been implemented")
