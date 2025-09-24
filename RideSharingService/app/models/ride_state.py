from abc import ABC, abstractmethod
from app.models.enums import RideStatus, UserType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ride import Ride
    from app.models.driver import Driver
    from app.models.user import User


class RideState(ABC):
    @abstractmethod
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def start_ride(self, ride: "Ride") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def complete_ride(self, ride: "Ride") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        raise NotImplementedError("Subclass must implement this method")


class RequestedState(RideState):
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        ride.set_driver(driver)
        ride.set_status(RideStatus.ACCEPTED)
        ride.set_state(AcceptedState())
        print(f"Ride {ride.get_id()} accepted by Driver:- {driver.get_name()}")

    def start_ride(self, ride: "Ride") -> None:
        print("Cannot start ride that is not accepted")

    def complete_ride(self, ride: "Ride") -> None:
        print("Cannot complete ride that is not in progress")

    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        ride.set_status(RideStatus.CANCELLED)
        ride.set_state(CancelledState())

        if cancelled_by.get_type() == UserType.RIDER:
            print(f"Ride {ride.get_id()} cancelled by Rider:- {cancelled_by.get_name()}")
        else:
            print(f"Ride {ride.get_id()} cancelled by Driver:- {cancelled_by.get_name()}")


class AcceptedState(RideState):
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        print("Ride already accepted")

    def start_ride(self, ride: "Ride") -> None:
        ride.set_status(RideStatus.IN_PROGRESS)
        ride.set_state(InProgressState())
        print(f"Ride {ride.get_id()} started")

    def complete_ride(self, ride: "Ride") -> None:
        print("Cannot complete ride that is not in progress")

    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        print("Cannot cancel ride that is accepted")


class InProgressState(RideState):
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        print("Ride already in progress")

    def start_ride(self, ride: "Ride") -> None:
        print("Ride is already in progress")

    def complete_ride(self, ride: "Ride") -> None:
        ride.set_status(RideStatus.COMPLETED)
        ride.set_state(CompletedState())
        print(f"Ride {ride.get_id()} completed")

    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        print("Cannot cancel ride that is in progress")


class CompletedState(RideState):
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        print("Ride already completed")

    def start_ride(self, ride: "Ride") -> None:
        print("Ride already completed")

    def complete_ride(self, ride: "Ride") -> None:
        print("Ride already completed")

    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        print("Cannot cancel completed ride")


class CancelledState(RideState):
    def accept_ride(self, ride: "Ride", driver: "Driver") -> None:
        print("Cannot accept cancelled ride")

    def start_ride(self, ride: "Ride") -> None:
        print("Cannot start cancelled ride")

    def complete_ride(self, ride: "Ride") -> None:
        print("Cannot complete cancelled ride")

    def cancel_ride(self, ride: "Ride", cancelled_by: "User") -> None:
        print("Ride already cancelled")
