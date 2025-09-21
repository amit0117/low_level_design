from app.models.booking import Booking
from app.seat_lock_manager import SeatLockManager
from app.models.user import User
from app.models.show import Show
from app.models.seat import Seat
from app.models.strategy.payment_strategy import PaymentStrategy


class BookingService:
    def __init__(self) -> None:
        self.seat_lock_manager = SeatLockManager()
        self.booking_history: dict[str, list[Booking]] = {}  # Append only on creation of booking

    # Create booking and mark the seats as locked for current user using lock manager
    def create_booking(self, user: User, show: Show, seats: list[Seat], payment_strategy: PaymentStrategy) -> Booking:
        booking = Booking(user, show, seats)
        if not self.seat_lock_manager.lock_seats(show, seats, user):
            return None
        user.update_booking_status(booking)
        # Add booking to the user's bookings history
        if user.id not in self.booking_history:
            self.booking_history[user.id] = []
        self.booking_history[user.id].append(booking)
        return booking

    # Confirm booking and mark the seats as booked
    def confirm_booking(self, booking: Booking) -> None:
        booking.confirm_booking()
        # Add booking to the user's bookings history
        booking.user.add_booking_to_history(booking)
        booking.user.update_booking_status(booking)
        # Unlock the seats
        self.seat_lock_manager.unlock_seats(booking.show, booking.seats, booking.user)

    # Cancel booking and mark the seats as available
    def cancel_booking(self, booking: Booking) -> None:
        booking.cancel_booking()
        # Remove booking from the user's bookings history
        booking.user.remove_booking_from_history(booking)
        booking.user.update_booking_status(booking)
        # Unlock the seats
        self.seat_lock_manager.unlock_seats(booking.show, booking.seats, booking.user)
