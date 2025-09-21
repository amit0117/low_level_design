from abc import ABC, abstractmethod
from app.models.enums import SeatStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.booking import Booking


class BookingState(ABC):
    @abstractmethod
    def confirm_booking(self, booking: "Booking") -> bool:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def cancel_booking(self, booking: "Booking") -> bool:
        raise NotImplementedError("Subclass must implement this method")


class PendingState(BookingState):
    def confirm_booking(self, booking: "Booking") -> bool:
        print(f"✅ Booking {booking.id} confirmed successfully")
        # Mark all seats as booked
        for seat in booking.seats:
            seat.set_status(SeatStatus.BOOKED)
        booking.set_state(ConfirmedState())
        return True

    def cancel_booking(self, booking: "Booking") -> bool:
        print(f"❌ Booking {booking.id} cancelled")
        # Mark all seats as available
        for seat in booking.seats:
            seat.set_status(SeatStatus.AVAILABLE)

        # Transition to cancelled state
        booking.set_state(CancelledState())
        return True


class ConfirmedState(BookingState):
    def confirm_booking(self, booking: "Booking") -> bool:
        print(f"❌ Cannot confirm confirmed booking {booking.id}")
        return False

    def cancel_booking(self, booking: "Booking") -> bool:
        print(f"❌ Booking {booking.id} cancelled")
        # Mark all seats as available
        for seat in booking.seats:
            seat.set_status(SeatStatus.AVAILABLE)

        # Transition to cancelled state
        booking.set_state(CancelledState())
        return True


class CancelledState(BookingState):
    def confirm_booking(self, booking: "Booking") -> bool:
        print(f"❌ Cannot confirm cancelled booking {booking.id}")
        return False

    def cancel_booking(self, booking: "Booking") -> bool:
        print(f"❌ Booking {booking.id} is already cancelled")
        return False
