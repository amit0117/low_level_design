from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.booking import Booking


class BookingObserver(ABC):
    @abstractmethod
    def update_booking_status(self, booking: "Booking") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class BookingSubject:
    def __init__(self):
        self.observers: list[BookingObserver] = []

    def add_observer(self, observer: BookingObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: BookingObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, booking: "Booking") -> None:
        for observer in self.observers:
            observer.update_booking_status(booking)
