from app.lock_manager import LockManager
from app.models.parking_spot import ParkingSpot
from app.models.enums import VehicleType
from app.models.vehicle import Vehicle


class Floor:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.parking_spots: dict[int, ParkingSpot] = {}
        self.lock_manager = LockManager()  # LockManager is used to manage locks of all parking spots of a level

    def get_floor_number(self) -> int:
        return self.floor_number

    def get_parking_spots(self) -> dict[int, ParkingSpot]:
        return self.parking_spots

    def add_parking_spot(self, parking_spot: ParkingSpot) -> None:
        self.parking_spots[parking_spot.get_spot_number()] = parking_spot

    def get_available_parking_spots(self, vehicle_type: VehicleType) -> list[ParkingSpot]:
        return [spot for spot in self.parking_spots.values() if spot.is_available() and spot.get_vehicle_type() == vehicle_type]

    def park_vehicle(self, spot_number: int, vehicle: Vehicle) -> bool:
        with self.lock_manager.acquire(spot_number):
            return self.parking_spots[spot_number].park_vehicle(vehicle)

    def unpark_vehicle(self, spot_number: int) -> bool:
        with self.lock_manager.acquire(spot_number):
            return self.parking_spots[spot_number].unpark_vehicle()

    def display_availability(self) -> None:
        print(f"Floor {self.floor_number} Availability:")
        for spot in self.parking_spots.values():
            print(f"Spot {spot.get_spot_number()}: {'Available' if spot.is_available() else 'Occupied'}")

    def get_parking_spot(self, spot_number: int) -> ParkingSpot:
        return self.parking_spots[spot_number]
