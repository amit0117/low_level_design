from typing import List, Set
from app.models.enums import PhaseType, Direction

class SignalPhase:

    def __init__(self, phase_type: PhaseType, allowed_directions: List[Direction], duration: int):
        self.phase_type = phase_type
        self.allowed_directions = set(allowed_directions)
        self.duration = duration

    def can_road_be_green(self, direction: Direction) -> bool:
        return direction in self.allowed_directions

    def conflicts_with(self, other_phase: "SignalPhase") -> bool:
        # Phases conflict if they have overlapping allowed directions
        # or if they allow perpendicular directions (e.g., North-South vs East-West)
        return bool(self.allowed_directions & other_phase.allowed_directions)

    def get_allowed_directions(self) -> Set[Direction]:
        return self.allowed_directions.copy()

    def __repr__(self) -> str:
        return f"SignalPhase(type={self.phase_type.value}, directions={[d.value for d in self.allowed_directions]}, duration={self.duration}s)"

class PhaseManager:

    @staticmethod
    def create_north_south_green_phase(duration: int = 30) -> SignalPhase:
        return SignalPhase(PhaseType.NORTH_SOUTH_GREEN, [Direction.NORTH, Direction.SOUTH], duration)

    @staticmethod
    def create_east_west_green_phase(duration: int = 30) -> SignalPhase:
        return SignalPhase(PhaseType.EAST_WEST_GREEN, [Direction.EAST, Direction.WEST], duration)

    @staticmethod
    def create_all_red_phase(duration: int = 2) -> SignalPhase:
        return SignalPhase(PhaseType.ALL_RED, [], duration)  # No directions allowed (all red)

    @staticmethod
    def create_emergency_phase(direction: Direction, duration: int = 60) -> SignalPhase:
        return SignalPhase(PhaseType.EMERGENCY_PHASE, [direction], duration)
