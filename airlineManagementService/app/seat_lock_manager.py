from app.models.seat import Seat
from typing import TYPE_CHECKING
import threading
import time

if TYPE_CHECKING:
    from app.models.user import User


class SeatLockManager:
    def __init__(self, flight_number: str):
        # store the locked seats who locked them
        # This will be used to unlock the seats after a timeout
        self.locked_seats: dict[Seat, "User"] = {}
        self.default_lock_timeout = 2  # For demonstration purposes only we kept it as 2 seconds, in real world, it would be in minutes
        self.flight_number = flight_number

    def lock_seats(self, seats: list[Seat], passenger: "User") -> bool:
        """
        Lock the seats for the given user
        Return True if the seats are locked successfully with atomicity, False otherwise
        """
        # Sort the seats to ensure consistent locking order to avoid race conditions and deadlocks
        sorted_seats = sorted(seats, key=lambda x: x.get_seat_number())
        print(
            f"Locking seats for {passenger.get_name()} on flight {self.flight_number}, seats: [{", ".join([seat.get_seat_number() for seat in sorted_seats])}]"
        )

        # First check if the seats are already locked by same user and return True if they are
        if all(seat in self.locked_seats and self.locked_seats[seat] == passenger for seat in sorted_seats):
            print(f"Seats are already locked by {passenger.get_name()} on flight {self.flight_number}, Returning True")
            return True

        # This will be used to unlock the seats if any error occurs because only the same user can unlock the seats
        # and is mandatory because if the same user has booked the seats in previous transaction and currently doing other transaction
        # and this time some error occurs, then we need to release the seats for the user for only this transaction
        # not for the previous transaction
        successfully_locked_seats: dict[Seat, "User"] = {}
        try:
            for seat in sorted_seats:
                # check if the seat is available and also check if the seat is already locked by other user
                # No need to check if the seat is locked by the same user, because even if there is stale data in the locked_seats ,i.e if someone has already release the lock manually without
                # seatLockManager so that seat will be available and the user for current seat will override the stale data
                # All these have been checked in the is_available() method of the seat class
                if not seat.is_available():
                    self.release_seats(successfully_locked_seats, passenger)
                    return False
                # lock the seat (Uses the state pattern to lock the seat)
                seat.lock_seat()
                successfully_locked_seats[seat] = passenger
                self.locked_seats[seat] = passenger  # will be used to unlock the seats after a timeout

        except Exception:
            print(f"Failed to lock seats for user {passenger.get_name()}")
            self.release_seats(successfully_locked_seats, passenger)
            return False
        else:
            print(f"All {len(sorted_seats)} seats locked successfully for user {passenger.get_name()}")
            # schedule a task to unlock the seats after a timeout (only once per transaction)
            self.release_seats_after_timeout(passenger)
            return True

    def release_seats_after_timeout(self, passenger: "User") -> None:
        """Schedule seat release after timeout using a separate thread"""

        def timeout_release():
            time.sleep(self.default_lock_timeout)
            self.release_seats(self.locked_seats, passenger)

        # Start the timeout in a separate thread to avoid blocking
        timeout_thread = threading.Thread(target=timeout_release, daemon=True)
        timeout_thread.start()

    def release_seats(self, locked_seats: dict[Seat, "User"], passenger: "User") -> None:
        # Create a copy of keys to avoid RuntimeError: dictionary changed size during iteration
        seats_to_release = list(locked_seats.keys())
        for seat in seats_to_release:
            # Check if the seat is locked by the same user
            # Also check if the seat is still locked, because calling release() on a seat that is not locked will raise an RuntimeError
            # Because it might possible that seat has been booked and user has already released the seat
            if self.locked_seats[seat] != passenger or not seat.get_lock().locked():
                continue
            seat.release_seat()
            # Remove the seat from the locked seats
            self.locked_seats.pop(seat)

    def get_passenger_locked_seats(self, passenger: "User") -> list[Seat]:
        """Get all seats locked by a specific user"""
        return [seat for seat, locked_user in self.locked_seats.items() if locked_user == passenger]
