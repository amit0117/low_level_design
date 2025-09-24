from abc import ABC, abstractmethod
from app.models.vehicle import Vehicle, Sedan, SUV, Luxury, Auto


class VehicleFactory(ABC):
    @abstractmethod
    def create_vehicle(self, license_plate: str, model: str) -> Vehicle:
        raise NotImplementedError("Subclasses must implement this method")


class AutoFactory(VehicleFactory):
    def create_vehicle(self, license_plate: str, model: str) -> Auto:
        return Auto(license_plate, model)


class SedanFactory(VehicleFactory):
    def create_vehicle(self, license_plate: str, model: str) -> Sedan:
        return Sedan(license_plate, model)


class SUVFactory(VehicleFactory):
    def create_vehicle(self, license_plate: str, model: str) -> SUV:
        return SUV(license_plate, model)


class LuxuryFactory(VehicleFactory):
    def create_vehicle(self, license_plate: str, model: str) -> Luxury:
        return Luxury(license_plate, model)
