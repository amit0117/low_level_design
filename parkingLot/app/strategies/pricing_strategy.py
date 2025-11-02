from abc import ABC, abstractmethod
from app.models.ticket import Ticket
from app.models.enums import VehicleType


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, ticket: Ticket) -> float:
        raise NotImplementedError("Subclasses must implement this method")


# There are several pricing strategies that can be implemented for a parking lot.
# 1. Flat-Rate Pricing
#     - A fixed fare for certain trips regardless of distance/time.
#     - Example: “₹300 flat from Airport to City Center.”
#     - In small parking lots, event parking, short term parking, etc.


# 2. Hourly Pricing
#     - Fare = (Rate per Hour * hours).
#     - In standard city parking lots, etc.
#     - Example: “₹100 per hour.”

# 3. Progressive Pricing
#     - Fare = (Rate per Hour * hours) + (Rate per Hour * hours * 1.5) + (Rate per Hour * hours * 2) ...i.e Cost increase with time duration
#     - Airport, Malls, Hight demand Areas, etc.
#     - Example: “₹100 per hour for first hour, ₹150 per hour for second hour, ₹200 per hour for third hour, etc.”

# 4. Vehicle based Pricing
#     - Fare = for bike: ₹10/ hour, for car: ₹20/ hour, for truck: ₹30/ hour, etc.


class FlatRatePricingStrategy(PricingStrategy):
    def __init__(self, flat_rate: int = 100):
        self.flat_rate = flat_rate

    def calculate_price(self, ticket: Ticket) -> float:
        return self.flat_rate


class HourlyPricingStrategy(PricingStrategy):
    def __init__(self, rate_per_hour: int = 10):
        self.rate_per_hour = rate_per_hour

    def calculate_price(self, ticket: Ticket) -> float:
        return self.rate_per_hour * ticket.get_duration().total_seconds() / 3600


class ProgressivePricingStrategy(PricingStrategy):
    def __init__(self, rate_per_hour: int = 10):
        self.rate_per_hour = rate_per_hour

    def calculate_price(self, ticket: Ticket) -> float:
        duration = ticket.get_duration().total_seconds()
        if duration <= 3600:
            return self.rate_per_hour * duration / 3600
        elif duration <= 7200:
            return self.rate_per_hour * 1.5 * duration / 3600
        elif duration <= 10800:
            return self.rate_per_hour * 2 * duration / 3600
        elif duration <= 14400:
            return self.rate_per_hour * 3 * duration / 3600
        else:
            return self.rate_per_hour * 4 * duration / 3600


class VehicleBasedPricingStrategy(PricingStrategy):
    def __init__(self, rate_per_hour: int = 10):
        self.rate_per_hour = {VehicleType.BIKE: 10, VehicleType.CAR: 20, VehicleType.TRUCK: 30}

    def calculate_price(self, ticket: Ticket) -> float:
        return self.get_rate_per_hour(ticket.get_vehicle().get_vehicle_type()) * ticket.get_duration().total_seconds() / 3600

    def get_rate_per_hour(self, vehicle_type: VehicleType) -> float:
        return self.rate_per_hour[vehicle_type]
