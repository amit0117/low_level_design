from uuid import uuid4
from app.models.enums import BookingStatus
from app.models.payment_result import PaymentResult
from app.models.flight import Flight
from app.models.seat import Seat
from app.observers.booking_observer import BookingSubject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import Passenger


class Booking(BookingSubject):
    def __init__(self, passenger: "Passenger", flight: Flight, seats: list[Seat], payment_result: PaymentResult):
        super().__init__()
        self.id = str(uuid4())
        self.passenger = passenger
        self.flight = flight
        self.seats = seats
        self.payment_result = payment_result
        self.status = BookingStatus.PENDING
        self.price = sum([seat.get_price() for seat in seats])
        # Add the passenger as an observer
        self.add_observer(passenger)

    def get_booking_id(self) -> str:
        return self.id

    def get_price(self) -> float:
        return self.price

    def get_flight(self) -> Flight:
        return self.flight

    def get_passenger(self) -> "Passenger":
        return self.passenger

    def get_seats(self) -> list[Seat]:
        return self.seats

    def get_booking_payment_result(self) -> PaymentResult:
        return self.payment_result

    def get_status(self) -> BookingStatus:
        return self.status

    def set_status(self, status: BookingStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def cancel(self) -> None:
        self.status = BookingStatus.CANCELLED
        for seat in self.seats:
            seat.release()

        # Also remove this user from the flight observers list
        self.flight.remove_observer(self.passenger)
