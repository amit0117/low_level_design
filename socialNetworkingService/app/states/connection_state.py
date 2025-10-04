from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import ConnectionStatus

if TYPE_CHECKING:
    from app.models.connection import Connection


class ConnectionState(ABC):
    @abstractmethod
    def send_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Not a valid transition from this state of connection")

    @abstractmethod
    def accept_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Not a valid transition from this state of connection")

    @abstractmethod
    def reject_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Not a valid transition from this state of connection")

    @abstractmethod
    def withdraw_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Not a valid transition from this state of connection")


class NotRequestedState(ConnectionState):
    def send_request(self, connection: "Connection") -> None:
        connection.set_status(ConnectionStatus.PENDING)
        connection.set_state(PendingState())

    def accept_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot accept a request that hasn't been sent")

    def reject_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot reject a request that hasn't been sent")

    def withdraw_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot withdraw a request that hasn't been sent")


class PendingState(ConnectionState):
    def send_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Request is already pending")

    def accept_request(self, connection: "Connection") -> None:
        connection.set_status(ConnectionStatus.ACCEPTED)
        connection.set_state(AcceptedState())

    def reject_request(self, connection: "Connection") -> None:
        print(f"{connection.get_to_user().get_name()} has rejected the request from {connection.get_from_user().get_name()}")
        connection.set_status(ConnectionStatus.REJECTED)
        connection.set_state(RejectedState())

    def withdraw_request(self, connection: "Connection") -> None:
        print(f"Request from {connection.get_from_user().get_name()} to {connection.get_to_user().get_name()} has been withdrawn")
        connection.set_status(ConnectionStatus.WITHDRAWN)
        connection.set_state(WithdrawnState())


class AcceptedState(ConnectionState):
    def send_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Connection is already accepted")

    def accept_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Connection is already accepted")

    def reject_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot reject an accepted connection")

    def withdraw_request(self, connection: "Connection") -> None:
        print(f"connection between {connection.get_from_user().get_name()} and {connection.get_to_user().get_name()} has been withdrawn")
        connection.set_status(ConnectionStatus.WITHDRAWN)
        connection.set_state(WithdrawnState())


class RejectedState(ConnectionState):
    def send_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot send request from rejected state")

    def accept_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot accept a rejected connection")

    def reject_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Connection is already rejected")

    def withdraw_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot withdraw a rejected connection")


class WithdrawnState(ConnectionState):
    def send_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot send request from withdrawn state")

    def accept_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot accept a withdrawn connection")

    def reject_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Cannot reject a withdrawn connection")

    def withdraw_request(self, connection: "Connection") -> None:
        raise NotImplementedError("Connection is already withdrawn")
