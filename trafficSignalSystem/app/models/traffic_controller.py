from typing import Optional, Dict
from app.models.intersection import Intersection
from app.models.signal_phase import PhaseManager
from app.strategies.timing_strategy import TimingStrategy, FixedTimingStrategy


class TrafficController:
    def __init__(self, intersection: Intersection, initial_strategy: Optional[TimingStrategy] = None):
        self.intersection = intersection
        self._strategy: TimingStrategy = initial_strategy or FixedTimingStrategy()
        self._phase_start_time = 0
        self._phases = [
            PhaseManager.create_north_south_green_phase(duration=30),
            PhaseManager.create_all_red_phase(duration=2),
            PhaseManager.create_east_west_green_phase(duration=30),
            PhaseManager.create_all_red_phase(duration=2),
        ]
        self._current_phase_index = 0

    def tick(self, current_time: int) -> None:
        self.intersection.tick()

        current_phase = self.intersection.get_active_phase()
        if current_phase is None:
            self._start_phase(0, current_time)
            return

        elapsed = current_time - self._phase_start_time
        duration = self._strategy.calculate_duration(current_phase, self.intersection)

        if elapsed >= duration:
            self._next_phase(current_time)

    def _start_phase(self, index: int, current_time: int) -> None:
        phase = self._phases[index]
        phase.duration = self._strategy.calculate_duration(phase, self.intersection)
        if self.intersection.transition_phase(phase):
            self._current_phase_index = index
            self._phase_start_time = current_time

    def _next_phase(self, current_time: int) -> None:
        self._current_phase_index = (self._current_phase_index + 1) % len(self._phases)
        self._start_phase(self._current_phase_index, current_time)

    def get_status(self) -> Dict:
        phase = self.intersection.get_active_phase()
        return {
            "strategy": type(self._strategy).__name__,
            "current_phase": phase.phase_type.value if phase else None,
        }
