# We will use decorator for adding different pricing strategies to the ride
# like discount (Coupon) and surge pricing, tax, etc.

from abc import ABC, abstractmethod
from app.strategies.pricing_strategy import PricingStrategy
from app.models.location import Location
from app.models.enums import RideType


class PricingDecorator(ABC):
    def __init__(self, pricing_strategy: PricingStrategy):
        self.pricing_strategy = pricing_strategy

    @abstractmethod
    # Provide the default implementation for the calculate_fare method in the base class
    # so that the subclasses can override it if needed
    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.pricing_strategy.calculate_fare(pickup, destination, ride_type)


class DiscountDecorator(PricingDecorator):
    def __init__(self, pricing_strategy: PricingStrategy, discount_percentage: float):
        super().__init__(pricing_strategy)
        self.discount_percentage = discount_percentage

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.pricing_strategy.calculate_fare(pickup, destination, ride_type) * (1 - self.discount_percentage)


class SurgeDecorator(PricingDecorator):
    def __init__(self, pricing_strategy: PricingStrategy, surge_multiplier: float):
        super().__init__(pricing_strategy)
        self.surge_multiplier = surge_multiplier

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.pricing_strategy.calculate_fare(pickup, destination, ride_type) * self.surge_multiplier


class TaxDecorator(PricingDecorator):
    def __init__(self, pricing_strategy: PricingStrategy, tax_percentage: float):
        super().__init__(pricing_strategy)
        self.tax_percentage = tax_percentage

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.pricing_strategy.calculate_fare(pickup, destination, ride_type) * (1 + self.tax_percentage)
