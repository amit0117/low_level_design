from app.models.user import User
from app.observers.ride_observer import RideObserver
from app.models.enums import UserType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ride import Ride


class Rider(User, RideObserver):
    def __init__(self, name: str, contact: str):
        super().__init__(name, contact, UserType.RIDER)

    def update_ride_status(self, ride: "Ride") -> None:
        print(f"--- Notification for Rider {self.get_name()} ---")
        print(f"  Trip {ride.get_id()} is now {ride.get_status().value}.")
        if ride.get_driver() is not None:
            print(
                f"  Driver: {ride.get_driver().get_name()} in a {ride.get_driver().get_vehicle().get_model()} "
                f"({ride.get_driver().get_vehicle().get_license_plate()})"
            )
        print("--------------------------------\n")
