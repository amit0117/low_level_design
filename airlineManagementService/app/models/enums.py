from enum import Enum


class SeatType(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST_CLASS = "FIRST_CLASS"


class SeatStatus(Enum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"


class BookingStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"


class FlightStatus(Enum):
    SCHEDULED = "SCHEDULED"
    BOARDING = "BOARDING"
    DEPARTED = "DEPARTED"
    IN_AIR = "IN_AIR"
    LANDED = "LANDED"
    ARRIVED = "ARRIVED"


class UserType(Enum):
    PASSENGER = "PASSENGER"
    AIRLINE_STAFF = "AIRLINE_STAFF"
    ADMIN = "ADMIN"


class PassengerType(Enum):
    REGULAR = "REGULAR"
    FREQUENT_FLYER = "FREQUENT_FLYER"
    CORPORATE = "CORPORATE"
    VIP = "VIP"


class StaffType(Enum):
    GROUND_STAFF = "GROUND_STAFF"
    CABIN_CREW = "CABIN_CREW"  # Flight Attendant
    COCKPIT_CREW = "COCKPIT_CREW"  # Pilot, Co-Pilot
    OTHER = "OTHER"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentMethod(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
