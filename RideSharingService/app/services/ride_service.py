from app.models.ride import Ride
from typing import Optional
from app.models.location import Location
from app.models.enums import RideType, RideStatus, PaymentStatus, PaymentMethod
from app.models.driver import Driver
from app.models.user import User
from app.models.payment_result import PaymentResult


class RideService:
    def __init__(self) -> None:
        self.rides: dict[str, Ride] = {}

    def add_ride(self, ride: Ride) -> None:
        self.rides[ride.get_id()] = ride

    def remove_ride(self, id: str) -> None:
        if id not in self.rides:
            print(f"Ride with id {id} not found")
            return
        del self.rides[id]

    def get_ride(self, id: str) -> Optional[Ride]:
        if id not in self.rides:
            print(f"Ride with id {id} not found")
            return None
        return self.rides[id]

    def get_all_rides(self) -> list[Ride]:
        return list(self.rides.values())

    def create_ride(self, rider: User, pickup: Location, destination: Location, ride_type: RideType, fare: float) -> Ride:
        # Create payment result
        payment = PaymentResult(fare, PaymentStatus.PENDING, PaymentMethod.UPI)

        # Create ride
        ride = Ride(rider, None, pickup, destination, RideStatus.REQUESTED, payment)
        return ride

    def accept_ride(self, driver: Driver, ride: Ride) -> None:
        # Add to the rides dictionary only if ride has accepted
        self.rides[ride.get_id()] = ride
        ride.accept_ride(driver)

    def start_ride(self, ride_id: str) -> None:
        ride = self.get_ride(ride_id)
        if ride is None:
            print(f"Ride with id {ride_id} not found")
            return
        ride.start_ride()

    def complete_ride(self, ride_id: str) -> None:
        ride = self.get_ride(ride_id)
        if ride is None:
            print(f"Ride with id {ride_id} not found")
            return
        ride.complete_ride()

    def cancel_ride(self, ride_id: str, cancelled_by: User) -> None:
        ride = self.get_ride(ride_id)
        if ride is None:
            print(f"Ride with id {ride_id} not found")
            return
        ride.cancel_ride(cancelled_by)
