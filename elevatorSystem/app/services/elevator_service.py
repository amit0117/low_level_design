import re
from app.models.elevator import Elevator
from app.models.request import Request
from app.repositories.elevator_repository import ElevatorRepository
from app.repositories.floor_repository import FloorRepository
from app.strategies.elevator_scheduling_strategy import ElevatorSchedulingStrategy, SCAN
from app.models.enums import Direction, RequestType
from threading import Lock
from app.models.floor import Floor
from concurrent.futures import ThreadPoolExecutor


class ElevatorService:
    instance = None
    lock = Lock()

    def __new__(cls, num_elevators: int = 4) -> "ElevatorService":
        if cls.instance is None:
            with cls.lock:
                if cls.instance is None:
                    cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, num_elevators: int = 4):
        if hasattr(self, "has_initialized") and self.has_initialized:
            return
        self.scheduling_strategy = SCAN()  # default scheduling strategy is SCAN
        self.elevator_repository = ElevatorRepository.get_instance()
        self.floor_repository = FloorRepository.get_instance()
        # keep floor from 1 to 10
        for floor in range(1, 11):
            self.floor_repository.save(Floor(floor))

        # Create elevators with capacity 1000kg
        for _ in range(1, num_elevators + 1):
            elevator = Elevator(capacity=1000)
            self.elevator_repository.save(elevator)

        # Use threadpool executor to start the elevators
        self.executor_service = ThreadPoolExecutor(max_workers=num_elevators)

        self.has_initialized = True

    @classmethod
    def get_instance(cls, num_elevators: int) -> "ElevatorService":
        return cls.instance or cls(num_elevators)

    def set_scheduling_strategy(self, scheduling_strategy: ElevatorSchedulingStrategy) -> None:
        self.scheduling_strategy = scheduling_strategy

    def start(self) -> None:
        print("Starting elevator system...")
        for elevator in self.elevator_repository.get_all_elevators():
            self.executor_service.submit(elevator.run)

    # --- Facade Methods ---
    # External Request (Hall Call)
    def request_elevator(self, floor_number: int, direction: Direction) -> Elevator:
        print(f"External Request: User at floor {floor_number} wants to go {direction.value}")
        request = Request(floor_number, direction, RequestType.EXTERNAL)
        selected_elevator = self.scheduling_strategy.select_elevator(self.elevator_repository.get_all_elevators(), request)
        if selected_elevator:
            selected_elevator.add_request_to_queue(request)
        else:
            raise ValueError("No elevator available")
        return selected_elevator

    # Internal Request (Cabin Call)
    def select_floor(self, elevator_id: str, destination_floor: int) -> Elevator:
        print(f"Internal Request: User in Elevator {elevator_id} selected floor {destination_floor}")
        request = Request(destination_floor, Direction.IDLE, RequestType.INTERNAL)
        elevator = self.elevator_repository.find_by_id(elevator_id)
        if elevator:
            elevator.add_request_to_queue(request)
        else:
            raise ValueError("No elevator available")
        return elevator

    def shutdown(self) -> None:
        print("Shutting down elevator system...")

        # Stop all elevators
        for elevator in self.elevator_repository.get_all_elevators():
            elevator.stop()

        # Shutdown the executor
        self.executor_service.shutdown(wait=False, cancel_futures=True)
        print("Elevator system shutdown complete.")
