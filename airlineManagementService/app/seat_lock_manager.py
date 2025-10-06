from app.models.seat import Seat
from typing import TYPE_CHECKING
import time

if TYPE_CHECKING:
    from app.models.user import User


class SeatLockManager:
    def __init__(self, flight_number: str):
        # store the locked seats who locked them
        # This will be used to unlock the seats after a timeout
        self.locked_seats: dict[Seat, "User"] = {}
        self.default_lock_timeout = 2  # For demonstration purposes only, in real world, it would be in minutes
        self.flight_number = flight_number

    def lock_seats(self, seats: list[Seat], passenger: "User") -> bool:
        """
        Lock the seats for the given user
        Return True if the seats are locked successfully with atomicity, False otherwise
        """
        # Sort the seats to ensure consistent locking order to avoid race conditions and deadlocks
        sorted_seats = sorted(seats, key=lambda x: x.get_seat_number())

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
                seat.lock()
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
        time.sleep(self.default_lock_timeout)
        self.release_seats(self.locked_seats, passenger)

    def release_seats(self, locked_seats: dict[Seat, "User"], passenger: "User") -> None:
        for seat in locked_seats:
            # Check if the seat is locked by the same user
            # Also check if the seat is still locked, because calling release() on a seat that is not locked will raise an RuntimeError
            # Because it might possible that seat has been booked and user has already released the seat
            if self.locked_seats[seat] != passenger or not seat.get_lock().locked():
                continue
            seat.release()
            # Remove the seat from the locked seats
            self.locked_seats.pop(seat)

    def get_passenger_locked_seats(self, passenger: "User") -> list[Seat]:
        """Get all seats locked by a specific user"""
        return [seat for seat, locked_user in self.locked_seats.items() if locked_user == passenger]
