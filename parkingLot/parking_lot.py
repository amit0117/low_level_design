from app.models.floor import Floor
from threading import Lock
from typing import Type
from app.models.parking_spot import ParkingSpot
from app.models.vehicle import Vehicle
from app.repositories.ticket_repository import TicketRepository
from app.models.enums import VehicleType
from app.repositories.gate_repository import GateRepository
from app.models.gate import EntryGate, ExitGate
from app.models.ticket import Ticket
from app.strategies.parking_spot_assignment_strategy import ParkingSpotAssignmentStrategy, RandomSpotAssignmentStrategy
from app.strategies.payment_strategy import PaymentStrategy, CashPaymentStrategy
from app.strategies.pricing_strategy import PricingStrategy, FlatRatePricingStrategy
from app.models.payment_response import PaymentResponse


class ParkingLot:
    _lock = Lock()
    _instance: "ParkingLot" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "floors"):
            return
        self.processing_lock = Lock()
        self.floors: dict[int, Floor] = dict()
        self.ticket_repository: TicketRepository = TicketRepository.get_instance()
        self.gate_repository: GateRepository = GateRepository.get_instance()
        self.parking_spot_assignment_strategy: ParkingSpotAssignmentStrategy = RandomSpotAssignmentStrategy()
        self.payment_strategy: PaymentStrategy = CashPaymentStrategy()
        self.pricing_strategy: PricingStrategy = FlatRatePricingStrategy()

    @classmethod
    def get_instance(cls: Type["ParkingLot"]) -> "ParkingLot":
        return cls._instance or cls()

    def add_floor(self, floor: Floor) -> None:
        self.floors[floor.get_floor_number()] = floor

    def add_parking_spot(self, floor_number: int, parking_spot: ParkingSpot) -> None:
        self.floors[floor_number].add_parking_spot(parking_spot)

    def get_floors(self) -> list[Floor]:
        return list(self.floors.values())

    def get_floor(self, floor_number: int) -> Floor:
        return self.floors[floor_number]

    def get_all_available_parking_spots(self, vehicle_type: VehicleType) -> dict[int, list[ParkingSpot]]:
        available_spots: dict[int, list[ParkingSpot]] = dict()
        for floor in self.floors.values():
            spots = floor.get_available_parking_spots(vehicle_type)
            if spots:
                available_spots[floor.get_floor_number()] = spots
        return available_spots

    def park_vehicle(self, vehicle: Vehicle, entry_gate_number: int) -> Ticket:
        return self.gate_repository.get_entry_gate(entry_gate_number).process_entry(vehicle)

    def unpark_vehicle(self, ticket_id: str, exit_gate_number: int) -> PaymentResponse:
        return self.gate_repository.get_exit_gate(exit_gate_number).process_exit(ticket_id)

    def display_availability(self) -> None:
        for floor in self.floors.values():
            floor.display_availability()

    def add_entry_gate(self, entry_gate: EntryGate) -> None:
        self.gate_repository.add_entry_gate(entry_gate)

    def add_exit_gate(self, exit_gate: ExitGate) -> None:
        self.gate_repository.add_exit_gate(exit_gate)

    def create_ticket(self, vehicle: Vehicle, parking_spot: ParkingSpot, entry_gate_number: int, floor_number: int) -> Ticket:
        return self.ticket_repository.create_ticket(vehicle, parking_spot, entry_gate_number, floor_number)

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self.ticket_repository.get_ticket(ticket_id)

    def allocate_parking_spot(self, vehicle: Vehicle) -> tuple[int, ParkingSpot]:
        available_spots = self.get_all_available_parking_spots(vehicle.get_vehicle_type())
        return self.parking_spot_assignment_strategy.assign_parking_spot(available_spots, vehicle)

    def calculate_price(self, ticket: Ticket) -> float:
        return self.pricing_strategy.calculate_price(ticket)

    def process_payment(self, ticket: Ticket) -> PaymentResponse:
        amount = self.calculate_price(ticket)
        return self.payment_strategy.pay(amount)
