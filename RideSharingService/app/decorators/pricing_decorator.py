# We will use decorator for adding different pricing strategies to the ride
# like discount (Coupon) and surge pricing, tax, etc.

from __future__ import annotations

from abc import ABC
from typing import Protocol

from app.models.location import Location
from app.models.enums import RideType


class FareCalculator(Protocol):
    """Structural type: anything that can compute a fare (base strategy or nested decorator)."""

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        ...


class PricingDecorator(ABC):
    """Wraps a FareCalculator (concrete PricingStrategy or another PricingDecorator)."""

    def __init__(self, wrapped: FareCalculator):
        self.wrapped = wrapped

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.wrapped.calculate_fare(pickup, destination, ride_type)


class DiscountDecorator(PricingDecorator):
    def __init__(self, wrapped: FareCalculator, discount_percentage: float):
        super().__init__(wrapped)
        self.discount_percentage = discount_percentage

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        base_fare = super().calculate_fare(pickup, destination, ride_type)
        return base_fare * (1 - self.discount_percentage)


class SurgeDecorator(PricingDecorator):
    def __init__(self, wrapped: FareCalculator, surge_multiplier: float):
        super().__init__(wrapped)
        self.surge_multiplier = surge_multiplier

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        base_fare = super().calculate_fare(pickup, destination, ride_type)
        return base_fare * self.surge_multiplier


class TaxDecorator(PricingDecorator):
    def __init__(self, wrapped: FareCalculator, tax_percentage: float):
        super().__init__(wrapped)
        self.tax_percentage = tax_percentage

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        base_fare = super().calculate_fare(pickup, destination, ride_type)
        return base_fare * (1 + self.tax_percentage)
