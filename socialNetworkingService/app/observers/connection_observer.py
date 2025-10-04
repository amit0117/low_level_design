from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import ConnectionStatus

if TYPE_CHECKING:
    from app.models.connection import Connection


class ConnectionObserver(ABC):
    @abstractmethod
    def update_on_request_sent(self, connection: "Connection") -> None:
        raise NotImplementedError("update_on_request_sent method is not implemented")

    @abstractmethod
    def update_on_request_accepted(self, connection: "Connection") -> None:
        raise NotImplementedError("update_on_request_accepted method is not implemented")


class ConnectionSubject:
    def __init__(self) -> None:
        self.observers: list[ConnectionObserver] = []

    def add_observer(self, observer: ConnectionObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: ConnectionObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, connection: "Connection") -> None:
        for observer in self.observers:
            if connection.get_status() == ConnectionStatus.PENDING:
                observer.update_on_request_sent(connection)
            elif connection.get_status() == ConnectionStatus.ACCEPTED:
                observer.update_on_request_accepted(connection)
