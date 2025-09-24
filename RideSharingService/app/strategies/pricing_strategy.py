# There are several pricing strategies that can be implemented for a ride sharing service.

# 1. Flat-Rate Pricing

#     -A fixed fare for certain trips regardless of distance/time.

#     -Example: “₹300 flat from Airport to City Center.”

#     -Good for predictability, reduces rider anxiety about fare variation.

# 2. Distance & Time-Based Pricing (Metered)

#     -Fare = Base Fare + (Per Km * distance) + (Per Minute * ride time).

#     -The most common pricing strategy, similar to traditional taxis.

# 3. Zone-Based / Corridor Pricing

#     -Predefined geographic zones with flat or fixed fares between them.

#     -Example: “Any ride within Zone A is ₹100; Zone A → Zone B is ₹200.”

#     -Works well in cities with high-density routes.

# 4. Vehicle/Class-Based Pricing

#     -Pricing varies by vehicle category (Economy, Sedan, SUV, Luxury, Bike, Auto).

#     -Example: Same trip may cost ₹120 (Bike), ₹200 (Sedan), ₹500 (SUV).

#     -Allows customer segmentation and higher margins.

# 5. Surge / Dynamic Pricing

#     - Prices increase when demand > supply (rain, rush hour, events).

#     -Example: 1.5x surge multiplier.

#     -Maximizes revenue, balances supply-demand, but often controversial.

# 6. Subscription / Pass-Based Pricing

#     -Riders pay a monthly fee for discounted rides.

#     -Example: UberPass, Ola Select – reduced surge, free cancellation, lower fares.

# 7. Pooling / Shared Ride Pricing

#     -Discounted fare if rider shares the trip with others.

#     -Example: UberPOOL, Ola Share – cheaper but with possible detours.

# 8. Time-of-Day / Peak vs Off-Peak Pricing

#     -Different base fares depending on time (night, rush hour, off-peak).

#     -Encourages demand shifting.

# 9. Distance Slab / Tiered Pricing

#     -Different per-km rates for different distance ranges.

#     -Example: First 5 km = ₹12/km, next 10 km = ₹10/km, beyond 15 km = ₹8/km.

#     -Encourages longer trips.

# 10. Bid/Auction-Based Pricing (Emerging)

#     -Riders can bid their price and drivers choose if they want to accept.

#     -More common in smaller/regional ride-hailing apps.

# 11. Event/Route-Specific Pricing

#     -Special pricing for major events or popular routes.

#     -Example: “Festival Ground → Metro Station = ₹100 fixed.”

#  In practice, companies often combine multiple strategies.
#     -For example:
#     -Final Price = Base Fare + Distance/Time Fare + Surge Multiplier – Subscription Discount


from abc import ABC, abstractmethod
from app.models.location import Location
from app.models.enums import RideType


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        raise NotImplementedError("Subclasses must implement this method")


class FlatRatePricingStrategy(PricingStrategy):
    def __init__(self, base_fare: float, flat_rate: float):
        self.base_fare = base_fare
        self.flat_rate = flat_rate

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        # For now, we are returning a fixed fare for all ride types
        return self.base_fare + self.flat_rate


class DistanceBasedPricingStrategy(PricingStrategy):
    def __init__(self, base_fare: float, rate_per_km: float):
        self.base_fare = base_fare
        self.rate_per_km = rate_per_km

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        return self.base_fare + self.rate_per_km * pickup.to_distance(destination)


class VehicleBasedPricingStrategy(PricingStrategy):
    def __init__(self, base_fare: float):
        self.base_fare = base_fare
        self.rate_per_km = {type.get_vehicle_type(): type.get_base_price() for type in RideType}

    def calculate_fare(self, pickup: Location, destination: Location, ride_type: RideType) -> float:
        # For now, we are returning a fixed fare for all ride types
        return self.base_fare + self.rate_per_km[ride_type.get_vehicle_type()] * pickup.to_distance(destination)
