# Same show can have different pricing based on the time of the day, day of the week, and the movie type
# Like morning shows: Lower price
# Evening shows: standard price
# Weekend shows: Premium price
# Vip shows: Luxury price

from abc import ABC, abstractmethod
from app.models.seat import Seat


class ShowPricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, seat: Seat) -> float:
        raise NotImplementedError("Subclass must implement this method")


class MorningPricingStrategy(ShowPricingStrategy):
    def __init__(self, morning_discount_percentage: float = 0.2):
        self.morning_discount_percentage = morning_discount_percentage

    def calculate_price(self, seat: Seat) -> float:
        return seat.type.price * (1 - self.morning_discount_percentage)


class EveningPricingStrategy(ShowPricingStrategy):
    # Assume evening pricing is the standard price
    def calculate_price(self, seat: Seat) -> float:
        return seat.type.price


class WeekendPricingStrategy(ShowPricingStrategy):
    def __init__(self, weekend_surcharge_percentage: float = 0.2):
        self.weekend_surcharge_percentage = weekend_surcharge_percentage

    def calculate_price(self, seat: Seat) -> float:
        return seat.type.price * (1 + self.weekend_surcharge_percentage)


class VipPricingStrategy(ShowPricingStrategy):
    def __init__(self, luxury_surcharge_percentage: float = 0.5):
        self.luxury_surcharge_percentage = luxury_surcharge_percentage

    def calculate_price(self, seat: Seat) -> float:
        return seat.type.price * (1 + self.luxury_surcharge_percentage)
