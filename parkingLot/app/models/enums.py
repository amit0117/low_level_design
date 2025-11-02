from enum import Enum


class VehicleType(Enum):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    TRUCK = "TRUCK"


class ParkingSpotStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"


class PaymentStatus(Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"

class PaymentMethod(Enum):
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"


class ParkingTicketStatus(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"


class GateType(Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
