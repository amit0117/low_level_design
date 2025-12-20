from typing import Dict, List, Optional, Set
from app.models.road import Road
from app.models.traffic_light import TrafficLight
from app.models.signal_phase import SignalPhase, PhaseManager
from app.models.enums import Direction
from app.states.traffic_light_state import RedState, YellowState, GreenState


class Intersection:
    def __init__(self, intersection_id: str):
        self.intersection_id = intersection_id
        self._roads: Dict[Direction, Road] = {}
        self._traffic_lights: Dict[Direction, TrafficLight] = {}
        self._current_phase: Optional[SignalPhase] = None
        self._phase_history: List[SignalPhase] = []

    def add_road(self, road: Road) -> None:
        if road.direction in self._roads:
            raise ValueError(f"Road with direction {road.direction.value} already exists")

        self._roads[road.direction] = road
        traffic_light = TrafficLight(road)
        road.set_traffic_light(traffic_light)
        self._traffic_lights[road.direction] = traffic_light

    def get_road(self, direction: Direction) -> Optional[Road]:
        return self._roads.get(direction)

    def get_traffic_light(self, direction: Direction) -> Optional[TrafficLight]:
        return self._traffic_lights.get(direction)

    def get_all_traffic_lights(self) -> List[TrafficLight]:
        return list(self._traffic_lights.values())

    def get_active_phase(self) -> Optional[SignalPhase]:
        return self._current_phase

    def can_transition(self, new_phase: SignalPhase) -> bool:
        # If no current phase, transition is always safe
        if self._current_phase is None:
            return True

        # Check if phases conflict
        if self._current_phase.conflicts_with(new_phase):
            return False

        # Additional safety: ensure all conflicting roads are red before new green
        # This is handled by the transition logic
        return True

    def transition_phase(self, new_phase: SignalPhase) -> bool:
        if not self.can_transition(new_phase):
            return False

        # First, set all traffic lights to red (safety measure)
        for direction, traffic_light in self._traffic_lights.items():
            traffic_light.force_transition_to(RedState())

        # Then, set allowed directions to green
        for direction in new_phase.get_allowed_directions():
            if direction in self._traffic_lights:
                traffic_light = self._traffic_lights[direction]
                green_state = GreenState(duration=new_phase.duration)
                traffic_light.force_transition_to(green_state)

        # Update current phase
        self._current_phase = new_phase
        self._phase_history.append(new_phase)

        return True

    def transition_to_yellow(self, directions: List[Direction]) -> None:
        yellow_state = YellowState()

        for direction in directions:
            if direction in self._traffic_lights:
                self._traffic_lights[direction].transition_to(yellow_state)

    def emergency_preempt(self, priority_direction: Direction) -> bool:
        if priority_direction not in self._traffic_lights:
            return False

        # Force all other directions to red
        for direction, traffic_light in self._traffic_lights.items():
            if direction != priority_direction:
                traffic_light.force_transition_to(RedState())

        # Set priority direction to green
        priority_light = self._traffic_lights[priority_direction]
        emergency_green = GreenState(duration=60)  # Extended duration for emergency
        priority_light.force_transition_to(emergency_green)

        # Update phase to emergency phase
        emergency_phase = PhaseManager.create_emergency_phase(priority_direction, duration=60)
        self._current_phase = emergency_phase

        return True

    def tick(self) -> None:
        for traffic_light in self._traffic_lights.values():
            traffic_light.tick()

    def get_conflicting_directions(self, direction: Direction) -> Set[Direction]:
        conflicts = set()

        # Perpendicular directions conflict
        if direction == Direction.NORTH or direction == Direction.SOUTH:
            conflicts.add(Direction.EAST)
            conflicts.add(Direction.WEST)
        elif direction == Direction.EAST or direction == Direction.WEST:
            conflicts.add(Direction.NORTH)
            conflicts.add(Direction.SOUTH)

        # Remove directions that don't exist in intersection
        return conflicts & set(self._roads.keys())

    def __repr__(self) -> str:
        return f"Intersection(id={self.intersection_id}, roads={len(self._roads)}, phase={self._current_phase.phase_type.value if self._current_phase else 'None'})"
