from abc import ABC, abstractmethod
from app.models.enums import SeatStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.seat import Seat


class SeatState(ABC):
    @staticmethod
    @abstractmethod
    def lock(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @staticmethod
    @abstractmethod
    def book(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @staticmethod
    @abstractmethod
    def release(seat: "Seat") -> None:
        raise NotImplementedError("Subclass must implement this method")


class AvailableState(SeatState):
    @staticmethod
    def lock(seat: "Seat") -> None:
        print(f"Seat :{seat.get_seat_number()} is locked.")
        seat.get_lock().acquire()  # acquire the lock
        seat.set_state(LockedState())
        seat.set_status(SeatStatus.LOCKED)

    @staticmethod
    def book(seat: "Seat") -> None:
        raise Exception("First we need to lock the seat. Can't book the seat without locking it.")

    @staticmethod
    def release(seat: "Seat") -> None:
        raise Exception("Seat is already available. No need to release it again.")


class LockedState(SeatState):
    @staticmethod
    def lock(seat: "Seat") -> None:
        raise Exception("Seat is already locked. No need to lock it again.")

    @staticmethod
    def book(seat: "Seat") -> None:
        print(f"Booking the seat :{seat.get_seat_number()}.")
        seat.set_state(ReservedState())
        seat.set_status(SeatStatus.RESERVED)

    @staticmethod
    def release(seat: "Seat") -> None:
        print(f"Releasing the seat :{seat.get_seat_number()}.")
        seat.set_state(AvailableState())
        seat.set_status(SeatStatus.AVAILABLE)
        seat.get_lock().release()  # release the lock


class ReservedState(SeatState):
    @staticmethod
    def lock(seat: "Seat") -> None:
        raise Exception("Seat is reserved. Can't lock the seat.")

    @staticmethod
    def book(seat: "Seat") -> None:
        raise Exception("Seat is already reserved. No need to book it again.")

    @staticmethod
    def release(seat: "Seat") -> None:
        print(f"Releasing the seat :{seat.get_seat_number()}.")
        seat.set_state(AvailableState())
        seat.set_status(SeatStatus.AVAILABLE)
        seat.get_lock().release()  # release the lock


class OccupiedState(SeatState):
    @staticmethod
    def lock(seat: "Seat") -> None:
        raise Exception("Seat is occupied. Can't lock the seat.")

    @staticmethod
    def book(seat: "Seat") -> None:
        raise Exception("Seat is occupied. No need to book it again.")

    @staticmethod
    def release(seat: "Seat") -> None:
        raise Exception("Seat is occupied. Can't release it.")
