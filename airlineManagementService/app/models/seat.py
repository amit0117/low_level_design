# Use per-seat locks, but handle multi-seat booking atomically, also implement a timeout for the locks

from threading import Lock
from app.models.enums import SeatStatus, SeatType
from app.states.seat_state import SeatState, AvailableState


class Seat:
    def __init__(self, seat_number: str, seat_type: SeatType):
        self.seat_number = seat_number
        self.seat_type = seat_type
        self._lock: Lock = Lock()  # per-seat locks
        self.timeout = 2  # timeout for the locks (for demo we have kept as 2 seconds), In real world, timeout would be in minutes
        self.status = SeatStatus.AVAILABLE
        self.state: SeatState = AvailableState()
        self.price = Seat.calculate_price(seat_type)

    @staticmethod
    def calculate_price(seat_type: SeatType) -> float:
        if seat_type == SeatType.ECONOMY:
            return 100
        elif seat_type == SeatType.PREMIUM_ECONOMY:
            return 150
        elif seat_type == SeatType.BUSINESS:
            return 200
        elif seat_type == SeatType.FIRST_CLASS:
            return 300

    def set_state(self, state: SeatState):
        self.state = state

    def set_status(self, status: SeatStatus):
        self.status = status

    def get_status(self) -> SeatStatus:
        return self.status

    def get_seat_number(self) -> str:
        return self.seat_number

    def get_seat_type(self) -> SeatType:
        return self.seat_type

    def get_price(self) -> float:
        return self.price

    def get_lock(self) -> Lock:
        return self._lock

    def is_available(self) -> bool:
        # VERY CRITICAL LOGIC
        # check if the seat is available and also check if the seat is already locked by other user due to concurrency
        return self.status == SeatStatus.AVAILABLE and not self.get_lock().locked()

    def lock_seat(self) -> None:
        print(f"Locking seat {self.get_seat_number()}")
        self.state.lock_seat(self)
        print(f"Locked seat {self.get_seat_number()}")

    def book_seat(self) -> None:
        print(f"Booking seat {self.get_seat_number()}")
        self.state.book_seat(self)
        print(f"Booked seat {self.get_seat_number()}")

    def release_seat(self) -> None:
        print(f"Releasing seat {self.get_seat_number()}")
        self.state.release_seat(self)
        print(f"Released seat {self.get_seat_number()}")
