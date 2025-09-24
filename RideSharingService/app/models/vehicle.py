from app.models.enums import VehicleType
from uuid import uuid4

class Vehicle:
    def __init__(self, license_plate: str, model: str, type: VehicleType):
        self.id = str(uuid4())
        self.license_plate = license_plate
        self.model = model
        self.type = type

    def get_license_plate(self) -> str:
        return self.license_plate

    def get_model(self) -> str:
        return self.model

    def get_type(self) -> VehicleType:
        return self.type

class Auto(Vehicle):
    def __init__(self, license_plate: str, model: str):
        super().__init__(license_plate, model, VehicleType.AUTO)

class Sedan(Vehicle):
    def __init__(self, license_plate: str, model: str):
        super().__init__(license_plate, model, VehicleType.SEDAN)

class SUV(Vehicle):
    def __init__(self, license_plate: str, model: str):
        super().__init__(license_plate, model, VehicleType.SUV)

class Luxury(Vehicle):
    def __init__(self, license_plate: str, model: str):
        super().__init__(license_plate, model, VehicleType.LUXURY)
