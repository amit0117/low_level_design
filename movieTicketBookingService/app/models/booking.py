from app.models.show import Show
from app.models.user import User
from app.models.seat import Seat
from uuid import uuid4
from app.models.booking_state import PendingState, BookingState
from app.models.enums import BookingStatus


class Booking:
    def __init__(self, user: User, show: Show, seats: list[Seat]):
        self._id = str(uuid4())
        self._user = user
        self._show = show
        self._seats = seats
        self._state = PendingState()
        self._status = BookingStatus.PENDING

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> User:
        return self._user

    @property
    def show(self) -> Show:
        return self._show

    @property
    def seats(self) -> list[Seat]:
        return self._seats

    @property
    def total_price(self) -> float:
        return sum(seat.type.price for seat in self._seats)

    @property
    def status(self) -> BookingStatus:
        return self._status

    def set_status(self, status: BookingStatus) -> None:
        self._status = status

    @property
    def state(self) -> BookingState:
        return self._state

    def set_state(self, state: BookingState) -> None:
        self._state = state

    def confirm_booking(self) -> bool:
        self.set_status(BookingStatus.CONFIRMED)
        return self.state.confirm_booking(self)

    def cancel_booking(self) -> bool:
        self.set_status(BookingStatus.CANCELLED)
        return self.state.cancel_booking(self)
