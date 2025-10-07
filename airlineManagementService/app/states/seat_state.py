from abc import ABC, abstractmethod
from app.models.enums import SeatStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.seat import Seat


class SeatState(ABC):
    @staticmethod
    @abstractmethod
    def lock_seat(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @staticmethod
    @abstractmethod
    def book_seat(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @staticmethod
    @abstractmethod
    def release_seat(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")


class AvailableState(SeatState):
    @staticmethod
    def lock_seat(seat: "Seat") -> None:
        # Use non-blocking acquire to avoid deadlock
        if seat.get_lock().acquire(blocking=False):
            seat.set_state(LockedState())
            seat.set_status(SeatStatus.LOCKED)
            print(f"Successfully acquired lock for seat {seat.get_seat_number()}")

        else:
            print(f"Failed to acquire lock for seat {seat.get_seat_number()} - already locked")
            raise Exception(f"Seat {seat.get_seat_number()} is already locked by another process")

    @staticmethod
    def book_seat(seat: "Seat") -> None:
        raise Exception("First we need to lock the seat. Can't book the seat without locking it.")

    @staticmethod
    def release_seat(seat: "Seat") -> None:
        raise Exception("Seat is already available. No need to release it again.")


class LockedState(SeatState):
    @staticmethod
    def lock_seat(seat: "Seat") -> None:
        raise Exception("Seat is already locked. No need to lock it again.")

    @staticmethod
    def book_seat(seat: "Seat") -> None:
        print(f"Booking the seat :{seat.get_seat_number()}.")
        seat.set_state(ReservedState())
        seat.set_status(SeatStatus.RESERVED)

    @staticmethod
    def release_seat(seat: "Seat") -> None:
        print(f"Releasing the seat :{seat.get_seat_number()}.")
        seat.set_state(AvailableState())
        seat.set_status(SeatStatus.AVAILABLE)
        if seat.get_lock().locked():
            seat.get_lock().release()  # release the lock


class ReservedState(SeatState):
    @staticmethod
    def lock_seat(seat: "Seat") -> None:
        raise Exception("Seat is reserved. Can't lock the seat.")

    @staticmethod
    def book_seat(seat: "Seat") -> None:
        raise Exception("Seat is already reserved. No need to book it again.")

    @staticmethod
    def release_seat(seat: "Seat") -> None:
        print(f"Releasing the seat :{seat.get_seat_number()}.")
        seat.set_state(AvailableState())
        seat.set_status(SeatStatus.AVAILABLE)
        if seat.get_lock().locked():
            seat.get_lock().release()  # release the lock


class OccupiedState(SeatState):
    @staticmethod
    def lock_seat(seat: "Seat") -> None:
        raise Exception("Seat is occupied. Can't lock the seat.")

    @staticmethod
    def book_seat(seat: "Seat") -> None:
        raise Exception("Seat is occupied. No need to book it again.")

    @staticmethod
    def release_seat(seat: "Seat") -> None:
        raise Exception("Seat is occupied. Can't release it.")
