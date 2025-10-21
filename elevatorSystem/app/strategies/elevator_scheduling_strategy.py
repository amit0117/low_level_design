from abc import ABC, abstractmethod
from app.models.enums import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.elevator import Elevator
    from app.models.request import Request


class ElevatorSchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators: "list[Elevator]", request: "Request") -> "Elevator":
        raise NotImplementedError("Subclasses must implement this method")


# There are several strategies for scheduling elevators:
# a) First Come First Serve (FCFS):
#   - Explanation:
#   - Serves requests in the order they are received. The the elevator simply moves to each requested floor in the given order.
#   - It's the simplest strategy but doesn't consider the current location or direction of the elevator, leading to potentially long, inefficient travel paths.
#   - Example:
#   - Initial State: Elevator is at Floor 5 and is idle.
#   - Requests (in order of arrival):
#   - Request from Floor 2 going UP.
#   - Request from Floor 8 going DOWN.
#   - Request from Floor 4 going UP.
#   - FCFS Path:
#   - The elevator moves from 5 to Floor 2 (to pick up Request 1).
#   - It then moves from 2 to Floor 8 (to pick up Request 2).
#   - It then moves from 8 to Floor 4 (to pick up Request 3).
#   - Trade-Off: The path is jagged (5 -> 2 -> 8 -> 4), wasting time and energy on unnecessary direction changes.

# b) Shortest Seek Time First (SSTF)
#   - Explanation:
#   - SSTF prioritizes the request that is closest to the elevator's current position, regardless of its direction. The "seek time" is the time it takes to reach the closest floor requesting service.
#   - It's a more efficient strategy than FCFS, as it minimizes the distance traveled by the elevator.
#   - Example:
#   - Initial State: Elevator is at Floor 5 and is idle.
#   - Requests (waiting):
#   - Floor 8 (Distance: 3 floors)
#   - Floor 3 (Distance: 2 floors)
#   - Floor 9 (Distance: 4 floors)
#   - SSTF Path:
#   - The closest request is Floor 3 (2 floors away). Elevator moves 5 to 3.
#   - From Floor 3, the closest waiting request is Floor 8 (5 floors away) OR Floor 9 (6 floors away). Elevator moves 3 to 8.
#   - The last request is Floor 9. Elevator moves 8 to 9.
#   - Trade-Off: While the next move is always optimal, requests far away (like Floor 9 in a scenario with continuous requests between 4 and 6) could be repeatedly delayed, leading to starvation.

# c) SCAN (Elevator Algorithm)
#   - Explanation:
#   - SCAN works like a classic disk scheduling algorithm. The elevator moves in a single direction (e.g., UP) servicing all requests in its path
#   - until it reaches the PHYSICAL LIMIT (top floor when going UP, bottom floor when going DOWN).
#   - It then reverses direction at the physical limit and repeats the process on the way back.
#   - Example Scenario:
#   - Imagine a 10-story building (Floors 1 to 10).
#   - Current Elevator Position: Floor 5
#   - Current Direction: UP
#   - Waiting Requests (floor: direction desired by passengers):
#   - 2: UP, 4: UP, 6: DOWN, 7: UP, 9: DOWN
#   - SCAN Path (Stops Only):
#   - Move UP from 5 and serve requests in ascending order: stop at 6, then 7, then 9.
#   - Continue to the PHYSICAL LIMIT (floor 10) even if no requests there, then reverse to DOWN.
#   - Move DOWN and serve remaining lower-floor requests in descending pass: stop at 4, then 2, and continue to the PHYSICAL LIMIT (floor 1).
#   - Sequence of stops: 6 -> 7 -> 9 -> 10 -> 4 -> 2 -> 1
#   - Notes:
#   - SCAN prioritizes direction continuity over immediate nearest requests, reducing direction changes.
#   - This improves overall throughput and fairness compared to SSTF by avoiding starvation for far-end floors.
#   - Trade-Off: Extra travel to physical limits can add overhead when extremes have no demand.
#   - Variant Note: LOOK is a related strategy that reverses at the furthest REQUESTED floor (not physical limit).

# d) LOOK
#   - Explanation:
#   - LOOK is an improvement on the SCAN algorithm. Instead of continuing all the way to the absolute end of the building (Floor 1 or Floor 10)
#   - when no requests exist past a certain point, the elevator reverses direction immediately upon reaching the last request in its current direction.
#   - Example:
#   - Initial State: Elevator is at Floor 5 and is moving UP.
#   - Requests (waiting):
#   - Pickup at Floor 7 (UP)
#   - Delivery at Floor 8 (Highest Request)
#   - Pickup at Floor 2 (Lowest Request)
#   - LOOK Path:
#   - The elevator moves UP from 5, services Floor 7 and reaches the last UP request at Floor 8.
#   - At Floor 8, it immediately reverses direction.
#   - It moves DOWN and services the request at Floor 2.
#   - SCAN vs. LOOK: If this were SCAN, the elevator would go past Floor 8 all the way to Floor 10 (the maximum floor) before reversing.
#   - LOOK saves time by reversing at Floor 8, avoiding the wasted travel time to Floors 9 and 10.


class FCFS(ElevatorSchedulingStrategy):
    def select_elevator(self, elevators: "list[Elevator]", request: "Request") -> "Elevator":
        if not elevators:
            raise ValueError("No elevators available")
        return elevators[0]


class SSTF(ElevatorSchedulingStrategy):
    def select_elevator(self, elevators: "list[Elevator]", request: "Request") -> "Elevator":
        if not elevators:
            raise ValueError("No elevators available")
        return min(elevators, key=lambda e: abs(e.get_current_floor_number() - request.target_floor_number))


class SCAN(ElevatorSchedulingStrategy):
    def select_elevator(self, elevators: "list[Elevator]", request: "Request") -> "Elevator":
        if not elevators:
            raise ValueError("No elevators available")
        best_elevator = None
        min_distance = float("inf")
        for elevator in elevators:
            if self._is_suitable(elevator, request):
                distance = abs(elevator.get_current_floor_number() - request.target_floor_number)
                if distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator

        return best_elevator or elevators[0]  # Fallback to first elevator if no suitable one found

    def _is_suitable(self, elevator: "Elevator", request: "Request") -> bool:
        if elevator.get_direction() == Direction.IDLE:
            return True
        if elevator.get_direction() == request.direction:
            if request.direction == Direction.UP and elevator.get_current_floor_number() <= request.target_floor_number:
                return True
            if request.direction == Direction.DOWN and elevator.get_current_floor_number() >= request.target_floor_number:
                return True
        return False
