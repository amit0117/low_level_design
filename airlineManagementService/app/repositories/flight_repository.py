from app.models.flight import Flight
from app.models.aircraft import Aircraft
from app.models.enums import FlightStatus
from typing import Optional
from threading import Lock
from datetime import datetime


class FlightRepository:
    _instance: Optional["FlightRepository"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "FlightRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "flights"):
            return
        self.flights: dict[str, Flight] = {}

    @classmethod
    def get_instance(cls: type["FlightRepository"]) -> "FlightRepository":
        return cls._instance or cls()

    def add_flight(self, flight: Flight) -> None:
        self.flights[flight.get_flight_number()] = flight

    def get_all_flights(self) -> list[Flight]:
        return list(self.flights.values())

    def get_all_flights_by_status(self, status: FlightStatus) -> list[Flight]:
        return [flight for flight in self.flights.values() if flight.get_status() == status]

    def get_all_flights_by_aircraft(self, aircraft: Aircraft) -> list[Flight]:
        return [flight for flight in self.flights.values() if flight.get_aircraft() == aircraft]

    def get_all_flights_between_source_and_destination(self, source: str, destination: str) -> list[Flight]:
        return [flight for flight in self.flights.values() if flight.get_source() == source and flight.get_destination() == destination]

    def get_all_flights_between_source_and_destination_within_a_date_range(
        self, source: str, destination: str, start_date: datetime, end_date: datetime
    ) -> list[Flight]:
        all_flights = self.get_all_flights_between_source_and_destination(source, destination)
        filtered_flights = [flight for flight in all_flights if flight.get_departure_time() >= start_date and flight.get_departure_time() <= end_date]
        return filtered_flights

    def get_flight_by_number(self, flight_number: str) -> Optional[Flight]:
        return self.flights.get(flight_number)
