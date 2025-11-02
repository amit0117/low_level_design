from threading import Lock
from app.models.ticket import Ticket
from typing import Type
from app.models.vehicle import Vehicle
from app.models.parking_spot import ParkingSpot


class TicketRepository:
    _lock = Lock()
    _instance: "TicketRepository" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "tickets"):
            return
        self.tickets: dict[str, Ticket] = {}

    @classmethod
    def get_instance(cls: Type["TicketRepository"]) -> "TicketRepository":
        return cls._instance or cls()

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self.tickets[ticket_id]

    def add_ticket(self, ticket: Ticket) -> None:
        self.tickets[ticket.get_ticket_id()] = ticket

    def update_ticket(self, ticket: Ticket) -> None:
        self.tickets[ticket.get_ticket_id()] = ticket

    def create_ticket(self, vehicle: Vehicle, parking_spot: ParkingSpot, entry_gate_number: int, floor_number: int) -> Ticket:
        ticket = Ticket(vehicle, parking_spot, entry_gate_number, floor_number)
        self.add_ticket(ticket)
        return ticket
