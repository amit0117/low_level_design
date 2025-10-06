from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.flight import Flight


class FlightObserver(ABC):

    @abstractmethod
    def update_flight_status(self, flight: "Flight") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class FlightSubject:
    def __init__(self):
        self.observers: list[FlightObserver] = []

    def add_observer(self, observer: FlightObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: FlightObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, flight: "Flight") -> None:
        for observer in self.observers:
            observer.update_flight_status(flight)
