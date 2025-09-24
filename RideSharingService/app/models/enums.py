from enum import Enum


class UserType(Enum):
    RIDER = "RIDER"
    DRIVER = "DRIVER"


class VehicleType(Enum):
    AUTO = "AUTO"  # (short for Auto-rickshaw in ride apps like Ola/Uber) → a 3-wheeler vehicle, cheaper, for short city trips, usually seats 2–3 passengers.
    SEDAN = "SEDAN"  # A 4-door passenger car with a separate trunk (e.g., Honda City, Toyota Corolla). Comfortable for 3–4 passengers with good legroom, typically used for city and intercity travel
    SUV = "SUV"  # (Support Utility Vehicle) larger, higher ground clearance, more powerful than sedans. Can seat 5–7 passengers, good for rough roads, long trips, and families (e.g., Toyota Fortuner, Hyundai Creta).
    LUXURY = "LUXURY"  # Refers to the premium category of vehicles (could be sedan, SUV, or hatchback) with high-end features, comfort, and brand value. Example: Mercedes-Benz, BMW, Audi.


class RideType(Enum):
    AUTO = (50, VehicleType.AUTO)
    SEDAN = (100, VehicleType.SEDAN)
    SUV = (150, VehicleType.SUV)
    LUXURY = (200, VehicleType.LUXURY)

    def __init__(self, base_price: float, vehicle_type: VehicleType):
        self.base_price = base_price
        self.vehicle_type = vehicle_type

    def get_base_price(self) -> float:
        return self.base_price

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type


class RideStatus(Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class DriverStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class PaymentMethod(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"
    CASH = "CASH"
