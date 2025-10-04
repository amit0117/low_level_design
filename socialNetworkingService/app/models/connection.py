from app.models.enums import ConnectionStatus
from typing import TYPE_CHECKING
from datetime import datetime
from app.states.connection_state import NotRequestedState, ConnectionState
from app.observers.connection_observer import ConnectionSubject

if TYPE_CHECKING:
    from app.models.user import User


class Connection(ConnectionSubject):
    def __init__(self, from_user: "User", to_user: "User"):
        super().__init__()
        self.from_user = from_user
        self.to_user = to_user
        self.requested_at = datetime.now()
        self.accepted_at = None
        self.status = ConnectionStatus.PENDING
        self.state: ConnectionState = NotRequestedState()
        # Add both from and to users as observers for this connection
        self.add_observer(from_user)
        self.add_observer(to_user)

    def set_status(self, status: ConnectionStatus) -> None:
        self.status = status
        if status == ConnectionStatus.ACCEPTED:
            self.accepted_at = datetime.now()
        self.notify_observers(self)

    def set_state(self, state: ConnectionState) -> None:
        self.state = state

    def get_from_user(self) -> "User":
        return self.from_user

    def get_to_user(self) -> "User":
        return self.to_user

    def get_status(self) -> ConnectionStatus:
        return self.status

    def get_requested_at(self) -> datetime:
        return self.requested_at

    def get_accepted_at(self) -> datetime:
        return self.accepted_at

    def get_state(self) -> ConnectionState:
        return self.state

    def send_request(self) -> None:
        self.state.send_request(self)

    def accept_request(self) -> None:
        self.state.accept_request(self)

    def reject_request(self) -> None:
        self.state.reject_request(self)

    def withdraw_request(self) -> None:
        self.state.withdraw_request(self)
