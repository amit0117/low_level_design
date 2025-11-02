from app.models.enums import GateType, ParkingTicketStatus
from app.models.vehicle import Vehicle
from app.models.ticket import Ticket
from datetime import datetime
from app.models.payment_response import PaymentResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parking_lot import ParkingLot


class Gate:
    def __init__(self, gate_number: int, gate_type: GateType, parking_lot: "ParkingLot"):
        self.gate_number = gate_number
        self.gate_type = gate_type
        self.parking_lot = parking_lot

    def get_gate_number(self) -> int:
        return self.gate_number

    def get_parking_lot(self) -> "ParkingLot":
        return self.parking_lot

    def get_gate_type(self) -> GateType:
        return self.gate_type

    def process_entry(self, vehicle: Vehicle, floor_number: int, spot_number: int) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def process_exit(self, ticket_id: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method")


class EntryGate(Gate):
    def __init__(self, gate_number: int):
        from parking_lot import ParkingLot
        parking_lot = ParkingLot.get_instance()
        super().__init__(gate_number, GateType.ENTRY, parking_lot)

    def process_entry(self, vehicle: Vehicle) -> Ticket:
        parking_lot = self.get_parking_lot()
        floor_number, parking_spot = parking_lot.allocate_parking_spot(vehicle)
        if floor_number is None or parking_spot is None:
            return None
        ticket = parking_lot.create_ticket(vehicle, parking_spot, self.get_gate_number(), floor_number)
        floor = parking_lot.get_floor(floor_number)
        floor.park_vehicle(parking_spot.get_spot_number(), vehicle)
        return ticket


class ExitGate(Gate):
    def __init__(self, gate_number: int):
        from parking_lot import ParkingLot
        parking_lot = ParkingLot.get_instance()
        super().__init__(gate_number, GateType.EXIT, parking_lot)

    def process_exit(self, ticket_id: str) -> PaymentResponse:
        parking_lot = self.get_parking_lot()
        ticket = parking_lot.get_ticket(ticket_id)

        payment_response = parking_lot.process_payment(ticket)
        # unpark the vehicle
        ticket.update_end_time(datetime.now())
        ticket.update_status(ParkingTicketStatus.PAID)
        floor = parking_lot.get_floor(ticket.get_floor_number())
        floor.unpark_vehicle(ticket.get_parking_spot().get_spot_number())
        return payment_response
