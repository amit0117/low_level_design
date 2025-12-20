from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import TrafficLightStatus

if TYPE_CHECKING:
    from app.models.traffic_light import TrafficLight


class TrafficLightState(ABC):
    @abstractmethod
    def get_status(self) -> TrafficLightStatus:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_duration(self) -> int:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def can_transition_to(self, new_state: "TrafficLightState") -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def on_timeout(self, traffic_light: "TrafficLight") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def on_enter(self, traffic_light: "TrafficLight") -> None:
        pass

    def __eq__(self, other) -> bool:
        return type(self) == type(other)

    def __hash__(self) -> int:
        return hash(type(self).__name__)


class RedState(TrafficLightState):
    def get_status(self) -> TrafficLightStatus:
        return TrafficLightStatus.RED

    def get_duration(self) -> int:
        # Red duration is typically long, but managed by phase timing
        return 30

    def can_transition_to(self, new_state: "TrafficLightState") -> bool:
        # Red can only transition to Yellow (when phase changes)
        return isinstance(new_state, YellowState)

    def on_timeout(self, traffic_light: "TrafficLight") -> None:
        # Red state timeout is handled by phase transitions, not automatic
        # The controller manages when to transition from Red
        pass

    def on_enter(self, traffic_light: "TrafficLight") -> None:
        # Log or perform actions when entering red state
        pass

    def __repr__(self) -> str:
        return "RedState()"


class YellowState(TrafficLightState):
    def __init__(self, duration: int = 3):
        self._duration = max(duration, 3)

    def get_status(self) -> TrafficLightStatus:
        return TrafficLightStatus.YELLOW

    def get_duration(self) -> int:
        return self._duration

    def can_transition_to(self, new_state: "TrafficLightState") -> bool:
        # Yellow can transition to Red (normal flow) or Green (emergency override)
        return isinstance(new_state, (RedState, GreenState))

    def on_timeout(self, traffic_light: "TrafficLight") -> None:
        # Yellow always transitions to Red after timeout

        traffic_light.transition_to(RedState())

    def on_enter(self, traffic_light: "TrafficLight") -> None:
        # Log or perform actions when entering yellow state
        pass

    def __repr__(self) -> str:
        return f"YellowState(duration={self._duration})"


class GreenState(TrafficLightState):
    def __init__(self, duration: int = 20):
        self._duration = duration

    def get_status(self) -> TrafficLightStatus:
        return TrafficLightStatus.GREEN

    def get_duration(self) -> int:
        return self._duration

    def can_transition_to(self, new_state: "TrafficLightState") -> bool:
        # Green can transition to Yellow (normal) or Red (emergency preemption)
        return isinstance(new_state, (YellowState, RedState))

    def on_timeout(self, traffic_light: "TrafficLight") -> None:
        # Green transitions to Yellow after timeout
        traffic_light.transition_to(YellowState())

    def on_enter(self, traffic_light: "TrafficLight") -> None:
        # Log or perform actions when entering green state
        pass

    def extend_duration(self, additional_seconds: int) -> None:
        self._duration += additional_seconds

    def __repr__(self) -> str:
        return f"GreenState(duration={self._duration})"
