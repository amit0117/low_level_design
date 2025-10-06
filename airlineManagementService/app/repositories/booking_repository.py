from app.models.booking import Booking
from typing import Optional
from threading import Lock
from app.models.enums import BookingStatus
from app.models.flight import Flight
from app.models.user import Passenger
from datetime import datetime


class BookingRepository:
    _instance: Optional["BookingRepository"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "BookingRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "bookings"):
            return
        self.bookings: dict[str, Booking] = {}

    @classmethod
    def get_instance(cls: type["BookingRepository"]) -> "BookingRepository":
        return cls._instance or cls()

    def add_booking(self, booking: Booking) -> None:
        self.bookings[booking.get_booking_id()] = booking

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        return self.bookings.get(booking_id)

    def get_all_bookings(self) -> list[Booking]:
        return list(self.bookings.values())

    def get_all_bookings_by_passenger(self, passenger: Passenger) -> list[Booking]:
        return [booking for booking in self.bookings.values() if booking.get_passenger() == passenger]

    def get_all_bookings_by_flight(self, flight: Flight) -> list[Booking]:
        return [booking for booking in self.bookings.values() if booking.get_flight() == flight]

    def get_all_bookings_by_status(self, status: BookingStatus) -> list[Booking]:
        return [booking for booking in self.bookings.values() if booking.get_status() == status]

    def get_all_bookings_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Booking]:
        return [
            booking
            for booking in self.bookings.values()
            if booking.get_flight().get_departure_time() >= start_date and booking.get_flight().get_arrival_time() <= end_date
        ]
