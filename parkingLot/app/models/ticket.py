from app.models.enums import ParkingTicketStatus
from datetime import datetime, timedelta
from app.models.vehicle import Vehicle
from app.models.parking_spot import ParkingSpot
from uuid import uuid4


class Ticket:
    def __init__(self, vehicle: Vehicle, parking_spot: ParkingSpot, entry_gate_number: int, floor_number: int):
        self.ticket_id = str(uuid4())
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.status = ParkingTicketStatus.ACTIVE
        self.start_time = datetime.now()
        self.end_time = None
        self.entry_gate_number = entry_gate_number
        self.floor_number = floor_number

    def get_entry_gate_number(self) -> int:
        return self.entry_gate_number

    def get_floor_number(self) -> int:
        return self.floor_number

    def get_ticket_id(self) -> str:
        return self.ticket_id

    def get_vehicle(self) -> Vehicle:
        return self.vehicle

    def get_parking_spot(self) -> ParkingSpot:
        return self.parking_spot

    def get_status(self) -> ParkingTicketStatus:
        return self.status

    def update_status(self, status: ParkingTicketStatus) -> None:
        self.status = status

    def get_start_time(self) -> datetime:
        return self.start_time

    def get_end_time(self) -> datetime:
        return self.end_time

    def update_end_time(self, end_time: datetime) -> None:
        self.end_time = end_time

    def get_duration(self) -> timedelta:
        return self.end_time - self.start_time
