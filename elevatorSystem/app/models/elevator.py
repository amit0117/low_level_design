from app.models.display_panel import DisplayPanel
from uuid import uuid4
from app.models.enums import ElevatorStatus, Direction, DoorStatus
from app.models.request import Request
from app.states.elevator_state import ElevatorState, IdleState
from threading import Lock
from app.repositories.floor_repository import FloorRepository
from app.observers.base_subject import BaseSubject


class Elevator(BaseSubject):
    def __init__(self, capacity: float) -> None:
        BaseSubject.__init__(self)
        self.id = str(uuid4())
        self.capacity = capacity
        self.display_panel = DisplayPanel(f"Elevator {self.id} Display")
        self.state: ElevatorState = IdleState()
        self.status = ElevatorStatus.IDLE
        self.direction = Direction.IDLE
        self.door_status = DoorStatus.CLOSED
        self.current_floor_number = 1  # Start at floor 1 instead of 0
        self.max_floor_number = 10
        self.min_floor_number = 0
        self.up_requests: set[Request] = set()
        self.down_requests: set[Request] = set()
        self.current_floor_number_lock = Lock()
        self.is_running = True
        # add all floor door panel as observers for this elevator
        for floor in FloorRepository.get_instance().get_all_floors():
            self.add_observer(floor.get_display_panel())
        # also add the display panel of this elevator as an observer for all floors
        self.add_observer(self.display_panel)

    def get_id(self) -> str:
        return self.id

    def get_max_floor_number(self) -> int:
        return self.max_floor_number

    def get_min_floor_number(self) -> int:
        return self.min_floor_number

    def get_up_requests(self) -> set[Request]:
        return self.up_requests

    def get_down_requests(self) -> set[Request]:
        return self.down_requests

    def get_current_floor_number(self) -> int:
        return self.current_floor_number

    def get_direction(self) -> Direction:
        return self.direction

    def get_status(self) -> ElevatorStatus:
        return self.status

    def get_door_status(self) -> DoorStatus:
        return self.door_status

    def set_state(self, state: ElevatorState) -> None:
        with self.current_floor_number_lock:
            self.state = state
            self.direction = state.get_direction()  # Update direction when state changes

    def set_status(self, status: ElevatorStatus) -> None:
        with self.current_floor_number_lock:
            self.status = status
            # Show appropriate message based on current state
            if self.direction == Direction.IDLE:
                message = f"Elevator {self.id} is now {status.value} and is idle at floor {self.current_floor_number}"
            else:
                message = f"Elevator {self.id} is now {status.value} and is moving {self.direction.value} at floor {self.current_floor_number}"
            self.notify_observers(message)

    def set_door_status(self, door_status: DoorStatus) -> None:
        with self.current_floor_number_lock:
            self.door_status = door_status

    def set_current_floor_number(self, floor_number: int) -> None:
        with self.current_floor_number_lock:
            self.current_floor_number = floor_number
            # Show appropriate message based on current state
            if self.direction == Direction.IDLE:
                message = f"Elevator {self.id} is now at floor {floor_number} and is idle"
            else:
                message = f"Elevator {self.id} is now at floor {floor_number} and is moving {self.direction.value}"
            self.notify_observers(message)

    def move(self) -> None:
        self.state.move(self)

    def add_request(self, request: Request) -> None:
        self.state.add_request(self, request)

    def get_direction(self) -> Direction:
        return self.state.get_direction()

    def run(self) -> None:
        while self.is_running:
            self.move()

            # Use very short sleep intervals to make shutdown more responsive
            for _ in range(20):  # Break 1 second into 20 x 0.05 second intervals
                if not self.is_running:
                    break
                try:
                    import time

                    time.sleep(0.05)
                except KeyboardInterrupt:
                    self.is_running = False
                    break

        print(f"Elevator {self.id[:8]}... has stopped.")

    def stop(self) -> None:
        with self.current_floor_number_lock:
            self.is_running = False
            self.set_status(ElevatorStatus.IDLE)
            self.set_state(IdleState())
