from typing import TYPE_CHECKING
from app.models.enums import TrafficLightStatus
from app.states.traffic_light_state import TrafficLightState, RedState, GreenState

if TYPE_CHECKING:
    from app.models.road import Road


class TrafficLight:
    def __init__(self, road: "Road"):
        self.road = road
        self._state: TrafficLightState = RedState()
        self._remaining_duration: int = 0
        self._state.on_enter(self)

    def get_current_state(self) -> "TrafficLightState":
        return self._state

    def get_status(self) -> TrafficLightStatus:
        return self._state.get_status()

    def get_remaining_duration(self) -> int:
        return max(0, self._remaining_duration)

    def transition_to(self, new_state: "TrafficLightState") -> bool:
        if self._state.can_transition_to(new_state):
            self._state = new_state
            self._remaining_duration = new_state.get_duration()
            self._state.on_enter(self)
            return True
        return False

    def tick(self) -> None:
        if self._remaining_duration > 0:
            self._remaining_duration -= 1
        if self._remaining_duration <= 0:
            self._state.on_timeout(self)

    def force_transition_to(self, new_state: "TrafficLightState") -> None:
        self._state = new_state
        self._remaining_duration = new_state.get_duration()
        self._state.on_enter(self)

    def extend_green(self, additional_seconds: int) -> None:
        if isinstance(self._state, GreenState):
            self._state.extend_duration(additional_seconds)
            self._remaining_duration += additional_seconds

    def __repr__(self) -> str:
        return f"TrafficLight(road={self.road.road_id}, state={self._state.get_status().value}, remaining={self._remaining_duration}s)"
