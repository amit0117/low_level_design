from abc import ABC, abstractmethod
from app.models.enums import RideStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ride import Ride


class RideObserver(ABC):
    @abstractmethod
    def update_ride_status(self, ride: "Ride") -> None:
        pass


class RiderObserver(RideObserver):
    def update_ride_status(self, ride: "Ride") -> None:
        print(f"--- Notification for Rider {self.get_name()} ---")
        print(f"  Trip {ride.get_id()} is now {ride.get_status().value}.")
        if ride.get_driver() is not None:
            print(
                f"  Driver: {ride.get_driver().get_name()} in a {ride.get_driver().get_vehicle().get_model()} "
                f"({ride.get_driver().get_vehicle().get_license_plate()})"
            )
        print("--------------------------------\n")


class DriverObserver(RideObserver):
    def update_ride_status(self, ride: "Ride") -> None:
        print(f"--- Notification for Driver {self.get_name()} ---")
        print(f"  Trip {ride.get_id()} is now {ride.get_status().value}.")
        if ride.get_status() == RideStatus.REQUESTED:
            print("  A new ride is available for you to accept.")
        print("--------------------------------\n")


class RideSubject:
    def __init__(self):
        self.observers: list[RideObserver] = []

    def add_observer(self, observer: RideObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: RideObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, ride: "Ride") -> None:
        for observer in self.observers:
            observer.update_ride_status(ride)
