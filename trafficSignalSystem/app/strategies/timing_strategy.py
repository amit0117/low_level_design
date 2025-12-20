from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import PhaseType

if TYPE_CHECKING:
    from app.models.intersection import Intersection
    from app.models.signal_phase import SignalPhase


class TimingStrategy(ABC):
    @abstractmethod
    def calculate_duration(self, phase: "SignalPhase", intersection: "Intersection") -> int:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def should_extend(self, phase: "SignalPhase", intersection: "Intersection", elapsed_time: int) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_max_duration(self, phase: "SignalPhase") -> int:
        raise NotImplementedError("Subclasses must implement this method")


class FixedTimingStrategy(TimingStrategy):
    def __init__(self, green_duration: int = 30, yellow_duration: int = 3, all_red_duration: int = 2):
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.all_red_duration = all_red_duration

    def calculate_duration(self, phase: "SignalPhase", intersection: "Intersection") -> int:
        if phase.phase_type == PhaseType.ALL_RED:
            return self.all_red_duration
        else:
            return self.green_duration

    def should_extend(self, phase: "SignalPhase", intersection: "Intersection", elapsed_time: int) -> bool:
        return False

    def get_max_duration(self, phase: "SignalPhase") -> int:
        return self.calculate_duration(phase, None)

    def __repr__(self) -> str:
        return f"FixedTimingStrategy(green={self.green_duration}s, yellow={self.yellow_duration}s)"


# there are other strategies like actuated timing strategy, emergency priority strategy, etc.
