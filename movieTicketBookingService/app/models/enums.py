from enum import Enum


class Genre(Enum):
    ACTION = "ACTION"
    COMEDY = "COMEDY"
    DRAMA = "DRAMA"
    HORROR = "HORROR"
    ROMANCE = "ROMANCE"
    SCIENCE_FICTION = "SCIENCE_FICTION"
    THRILLER = "THRILLER"
    ANIMATION = "ANIMATION"
    BIOGRAPHY = "BIOGRAPHY"


class BookingStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    LOCKED = "LOCKED"  # Temporarily held during booking process to prevent race conditions


class SeatType(Enum):
    REGULAR = (50.0, "REGULAR")
    PREMIUM = (80.0, "PREMIUM")
    RECLINER = (120.0, "RECLINER")

    def __init__(self, price: float, name: str):
        self._price = price
        self._name = name

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name
