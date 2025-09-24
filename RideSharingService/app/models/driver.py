from app.models.user import User
from app.models.ride import Ride
from app.models.location import Location
from app.models.enums import DriverStatus, VehicleType, UserType
from app.models.vehicle import Vehicle
from app.observers.ride_observer import DriverObserver


class Driver(User, DriverObserver):
    def __init__(self, name: str, contact: str, vehicle: Vehicle, location: Location):
        super().__init__(name, contact, UserType.DRIVER)
        self.current_location: Location = location
        self.status: DriverStatus = DriverStatus.OFFLINE
        self.vehicle: Vehicle = vehicle
        self.total_earnings: float = 0.0

    def accept_ride(self, ride: Ride) -> None:
        pass

    def cancel_ride(self, ride: Ride) -> None:
        pass

    def set_status(self, status: DriverStatus) -> None:
        self.status = status

    def get_status(self) -> DriverStatus:
        return self.status

    def get_vehicle(self) -> Vehicle:
        return self.vehicle

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle.type

    def get_current_location(self) -> Location:
        return self.current_location

    def set_current_location(self, location: Location) -> None:
        self.current_location = location

    def get_total_earnings(self) -> float:
        return self.total_earnings

    def add_earnings(self, earnings: float) -> None:
        self.total_earnings += earnings
