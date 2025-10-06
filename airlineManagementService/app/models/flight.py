from app.models.seat import Seat
from app.models.aircraft import Aircraft
from datetime import datetime
from app.models.enums import FlightStatus
from app.observers.flight_observer import FlightSubject
from typing import TYPE_CHECKING
from app.seat_lock_manager import SeatLockManager

if TYPE_CHECKING:
    from app.models.user import User


class Flight(FlightSubject):
    def __init__(self, flight_number: str, aircraft: Aircraft, source: str, destination: str, departure_time: datetime, arrival_time: datetime):
        super().__init__()
        self.flight_number = flight_number
        self.aircraft = aircraft
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        # store the seats in a dictionary with seat number as key
        self.seats: dict[int, Seat] = {}
        self.status = FlightStatus.SCHEDULED
        self.seat_lock_manager = SeatLockManager(flight_number)

    def get_available_seats(self) -> list[Seat]:
        return [seat for seat in self.seats.values() if seat.is_available()]

    def get_status(self) -> FlightStatus:
        return self.status

    def get_flight_number(self) -> str:
        return self.flight_number

    def get_all_seats(self) -> dict[int, Seat]:
        return self.seats

    def get_aircraft(self) -> Aircraft:
        return self.aircraft

    def get_source(self) -> str:
        return self.source

    def get_destination(self) -> str:
        return self.destination

    def get_departure_time(self) -> datetime:
        return self.departure_time

    def get_arrival_time(self) -> datetime:
        return self.arrival_time

    def set_status(self, status: FlightStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def add_seat(self, seat: Seat) -> None:
        # Check if we have already reached the maximum number of seats
        if len(self.seats) >= self.aircraft.get_total_seats():
            raise Exception("Maximum number of seats reached")
        self.seats[seat.get_seat_number()] = seat

    def lock_seats(self, seats: list[Seat], passenger: "User") -> bool:
        return self.seat_lock_manager.lock_seats(seats, passenger)

    def book_seats(self, seats: list[Seat], passenger: "User") -> None:
        # This should be called only if the seats are locked successfully
        for seat in seats:
            seat.book()
        # Add the passenger to the observers list
        self.add_observer(passenger)

    def release_seats(self, seats: list[Seat], passenger: "User") -> None:
        self.seat_lock_manager.release_seats(seats, passenger)

    def get_locked_seats_by_passenger(self, passenger: "User") -> list[Seat]:
        return self.seat_lock_manager.get_passenger_locked_seats(passenger)
