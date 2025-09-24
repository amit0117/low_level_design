from app.services.ride_service import RideService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
from threading import Lock
from app.strategies.driver_matching_strategy import DriverMatchingStrategy, NearestDriverMatchingStrategy
from app.models.vehicle import Vehicle
from app.models.location import Location
from app.models.user import User
from app.models.driver import Driver
from app.models.enums import RideType, DriverStatus
from app.models.ride import Ride
from typing import Optional
from app.decorators.pricing_decorator import PricingDecorator


class RideSharingSystem:
    _lock = Lock()
    _instance = None

    def __new__(cls) -> "RideSharingSystem":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return
        self.ride_service = RideService()
        self.payment_service = PaymentService()
        self.user_service = UserService()
        self.driver_matching_strategy = NearestDriverMatchingStrategy()  # Default strategy is NearestDriverMatchingStrategy
        self.processing_lock = Lock()
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "RideSharingSystem":
        return cls()

    def set_driver_matching_strategy(self, strategy: DriverMatchingStrategy) -> None:
        self.driver_matching_strategy = strategy

    def get_driver_matching_strategy(self) -> DriverMatchingStrategy:
        return self.driver_matching_strategy

    def get_ride_service(self) -> RideService:
        return self.ride_service

    def get_payment_service(self) -> PaymentService:
        return self.payment_service

    def get_user_service(self) -> UserService:
        return self.user_service

    def register_rider(self, name: str, contact: str) -> User:
        return self.user_service.add_rider(name, contact)

    def register_driver(self, name: str, contact: str, vehicle: Vehicle, location: Location) -> Driver:
        return self.user_service.add_driver(name, contact, vehicle, location)

    def request_ride(
        self, rider_id: str, pickup: Location, destination: Location, ride_type: RideType, pricing_decorator: PricingDecorator
    ) -> Optional[Ride]:

        # Validate for the rider
        if not self.user_service.does_user_exist(rider_id):
            print(f"Rider with id {rider_id} does not exist")
            return None

        # Find the available drivers using driver matching strategy
        available_drivers = self.driver_matching_strategy.get_available_drivers(self.user_service.all_drivers(), pickup, ride_type)
        if len(available_drivers) == 0:
            print("No available drivers found for the requested ride.")
            return None

        # Calculate the fare using pricing strategy
        fare = pricing_decorator.calculate_fare(pickup, destination, ride_type)
        # Create a ride using the ride service
        rider = self.user_service.get_user_by_id(rider_id)
        ride = self.ride_service.create_ride(rider, pickup, destination, ride_type, fare)

        # Notify the nearby drivers about the new ride request to accept or reject
        for driver in available_drivers:
            driver.update_ride_status(ride)

        return ride

    def accept_ride(self, driver_id: str, ride: Ride) -> None:
        driver = self.user_service.get_user_by_id(driver_id)
        if driver is None:
            print(f"Driver with id {driver_id} not found")
            return
        with self.processing_lock:
            self.ride_service.accept_ride(driver, ride)
            ride.get_driver().set_status(DriverStatus.BUSY)
            # Add the ride to the driver's and rider's ride history
            driver.add_ride_to_history(ride)
            ride.get_rider().add_ride_to_history(ride)
            print(f"Driver {driver.get_name()} accepted ride {ride.get_id()}")

    def start_ride(self, ride_id: str) -> None:
        with self.processing_lock:
            self.ride_service.start_ride(ride_id)

    def complete_ride(self, ride_id: str) -> None:
        with self.processing_lock:
            self.ride_service.complete_ride(ride_id)
            # mark the driver as available
            ride = self.ride_service.get_ride(ride_id)
            ride.get_driver().set_status(DriverStatus.AVAILABLE)
            print(f"Driver {ride.get_driver().get_name()} completed ride {ride.get_id()} and is now available.")

    def cancel_ride(self, ride_id: str, cancelled_by: User) -> None:
        with self.processing_lock:
            self.ride_service.cancel_ride(ride_id, cancelled_by)
            ride = self.ride_service.get_ride(ride_id)
            ride.get_driver().set_status(DriverStatus.AVAILABLE)
            print(f"Driver {ride.get_driver().get_name()} cancelled ride {ride.get_id()} and is now available.")
