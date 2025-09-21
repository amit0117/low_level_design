from app.models.show import Show
from app.models.seat import Seat
from app.models.user import User
from app.models.enums import SeatStatus
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import time


# We will use threadpool executor to schedule the task to unlock the seats after a timeout
class SeatLockManager:
    def __init__(self):
        self.max_workers = 5
        self.lock_timeout = 2  # 2 seconds
        self.locked_seats: dict[Show, dict[Seat, User]] = defaultdict(dict)
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

    def lock_seats(self, show: Show, seats: list[Seat], user: User) -> bool:
        # We will use Show's instance level lock to ensure atomicity for that specific show
        # Because if we use class level lock, then multiple shows will be locked and we will not be able to lock the seats for that show
        if getattr(show, "_lock", None) is None:
            show_lock = Lock()
            setattr(show, "_lock", show_lock)
        with show._lock:
            # Check if any of the requested seats are already locked or booked
            for seat in seats:
                if seat.status != SeatStatus.AVAILABLE:
                    print(f"Seat {seat.id} ,row {seat.row} ,column {seat.col} is not available. Locking failed.")
                    return False

            # Lock the seats and mark the locked seats in the name of current user
            for seat in seats:
                seat.set_status(SeatStatus.LOCKED)
                self.locked_seats[show][seat] = user

            # Schedule a task to unlock the seats after a timeout (Just in case the booking is not confirmed or user is not able to pay)
            self.executor.submit(self.unlock_seats_impl, show, seats, user)
            return True

    def unlock_seats_impl(self, show: Show, seats: list[Seat], user: User):
        time.sleep(self.lock_timeout)
        self.unlock_seats(show, seats, user)

    def unlock_seats(self, show: Show, seats: list[Seat], user: User) -> None:
        # Check if these seats are still locked by the same user, And we will use the same lock
        # First Check if there is lock for the show, if not return because if these seats were locked for current show then that show must have lock
        if getattr(show, "_lock", None) is None:
            return

        with show._lock:
            if self.locked_seats.get(show, None) is None:
                return
            locked_seats = self.locked_seats[show]
            # Check if the seats are still locked by the same user (The current implementation supports partial booking but in real world, we will not allow partial booking)
            for seat in seats:
                if seat in locked_seats and locked_seats[seat] == user:
                    if seat.status == SeatStatus.LOCKED:
                        print(f"Unlocked seat: {seat.id} ,row {seat.row} ,column {seat.col} due to timeout.")
                        seat.set_status(SeatStatus.AVAILABLE)
                    else:
                        print(f"Unlocked seat: {seat.id} ,row {seat.row} ,column {seat.col} due to booking completion.")
                    del locked_seats[seat]
            # If there are no locked seats for the show, then remove the show from the locked_seats dictionary
            if len(locked_seats) == 0:
                del self.locked_seats[show]

    def get_user_locked_seats(self, show: Show, user_id: str) -> list[Seat]:
        """Get all seats locked by a specific user in a show"""
        if show not in self.locked_seats:
            return []

        show_locks = self.locked_seats[show]
        return [seat for seat, locked_user_id in show_locks.items() if locked_user_id == user_id]
