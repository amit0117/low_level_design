from app.models.enums import ParkingSpotStatus, VehicleType
from app.models.vehicle import Vehicle


class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type: VehicleType):
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.status = ParkingSpotStatus.AVAILABLE
        self.vehicle = None

    def is_available(self) -> bool:
        return self.status == ParkingSpotStatus.AVAILABLE

    def get_spot_number(self) -> int:
        return self.spot_number

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_available() and vehicle.get_vehicle_type() == self.vehicle_type:
            self.vehicle = vehicle
            self.status = ParkingSpotStatus.OCCUPIED
            return True
        else:
            return False

    def unpark_vehicle(self) -> bool:
        if self.is_available():
            return False
        else:
            self.vehicle = None
            self.status = ParkingSpotStatus.AVAILABLE
            return True
