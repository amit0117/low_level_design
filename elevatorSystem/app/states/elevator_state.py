from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.request import Request
from app.models.enums import Direction, RequestType, ElevatorStatus

if TYPE_CHECKING:
    from app.models.elevator import Elevator


class ElevatorState(ABC):
    @abstractmethod
    def move(self, elevator: "Elevator"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def add_request(self, elevator: "Elevator", request: Request):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_direction(self) -> Direction:
        raise NotImplementedError("Subclasses must implement this method")


class IdleState(ElevatorState):
    def move(self, elevator: "Elevator") -> None:
        # Check if there are any requests
        if elevator.get_up_requests():
            elevator.set_state(MovingUpState())
            elevator.set_status(ElevatorStatus.MOVING)
            elevator.set_direction(Direction.UP)
        elif elevator.get_down_requests():
            elevator.set_state(MovingDownState())
            elevator.set_status(ElevatorStatus.MOVING)
            elevator.set_direction(Direction.DOWN)
        # Else stay idle - no requests to process

    def add_request(self, elevator: "Elevator", request: Request) -> None:
        # for Idle directly add to the appropriate queue
        if request.target_floor_number > elevator.get_current_floor_number():
            elevator.get_up_requests().add(request)
        elif request.target_floor_number < elevator.get_current_floor_number():
            elevator.get_down_requests().add(request)
        # If request is for current floor, doors would open (handled implicitly by moving to that floor)

    def get_direction(self) -> Direction:
        return Direction.IDLE


class MovingUpState(ElevatorState):
    def move(self, elevator: "Elevator") -> None:
        # If no UP requests or reached max floor, transition to IdleState
        if not elevator.get_up_requests() or elevator.get_current_floor_number() == elevator.get_max_floor_number():
            elevator.set_state(IdleState())
            elevator.set_status(ElevatorStatus.IDLE)
            elevator.set_direction(Direction.IDLE)
            return

        # Move up one floor
        elevator.set_current_floor_number(elevator.get_current_floor_number() + 1)

        # Check if we've reached any UP requests
        requests_to_remove = []
        for request in elevator.get_up_requests():
            if elevator.get_current_floor_number() == request.target_floor_number:
                requests_to_remove.append(request)

        # Remove completed requests
        for request in requests_to_remove:
            elevator.get_up_requests().remove(request)

        # If no more UP requests, transition to IdleState to check for DOWN requests
        if not elevator.get_up_requests():
            elevator.set_state(IdleState())
            elevator.set_status(ElevatorStatus.IDLE)
            elevator.set_direction(Direction.IDLE)
            return

    def add_request(self, elevator: "Elevator", request: Request) -> None:
        # Internal requests always get added to the appropriate queue
        if request.type == RequestType.INTERNAL:
            if request.target_floor_number > elevator.get_current_floor_number():
                elevator.get_up_requests().add(request)
            else:
                elevator.get_down_requests().add(request)
            return

        # External requests (will only be added if it's going in the same direction as the elevator)
        if request.direction == Direction.UP and request.target_floor_number >= elevator.get_current_floor_number():
            elevator.get_up_requests().add(request)
        elif request.direction == Direction.DOWN:  # Otherwise add to the down requests
            elevator.get_down_requests().add(request)

    def get_direction(self) -> Direction:
        return Direction.UP


class MovingDownState(ElevatorState):
    def move(self, elevator: "Elevator") -> None:
        # If no DOWN requests or reached min floor, transition to IdleState
        if not elevator.get_down_requests() or elevator.get_current_floor_number() == elevator.get_min_floor_number():
            elevator.set_state(IdleState())
            elevator.set_status(ElevatorStatus.IDLE)
            elevator.set_direction(Direction.IDLE)
            return

        # Move down one floor
        elevator.set_current_floor_number(elevator.get_current_floor_number() - 1)

        # Check if we've reached any DOWN requests
        requests_to_remove = []
        for request in elevator.get_down_requests():
            if elevator.get_current_floor_number() == request.target_floor_number:
                requests_to_remove.append(request)

        # Remove completed requests
        for request in requests_to_remove:
            elevator.get_down_requests().remove(request)

        # If no more DOWN requests, transition to IdleState to check for UP requests
        if not elevator.get_down_requests():
            elevator.set_state(IdleState())
            elevator.set_status(ElevatorStatus.IDLE)
            elevator.set_direction(Direction.IDLE)

    def add_request(self, elevator: "Elevator", request: Request) -> None:
        # Internal requests always get added to the appropriate queue
        if request.type == RequestType.INTERNAL:
            if request.target_floor_number > elevator.get_current_floor_number():
                elevator.get_up_requests().add(request)
            else:
                elevator.get_down_requests().add(request)
            return

        # External requests (will only be added if it's going in the same direction as the elevator)
        if request.direction == Direction.DOWN and request.target_floor_number <= elevator.get_current_floor_number():
            elevator.get_down_requests().add(request)
        elif request.direction == Direction.UP:
            elevator.get_up_requests().add(request)

    def get_direction(self) -> Direction:
        return Direction.DOWN
