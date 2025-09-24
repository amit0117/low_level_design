# There are several strategies to match drivers to a ride request
# 1. Nearest Driver Matching Strategy

#     -Match the nearest driver to the ride request.

# 2. First-Come-First-Served (FCFS) Driver Matching Strategy

#     -Match the first available driver in the system’s queue.

#     -Ensures fairness for drivers but may lead to suboptimal pickup times.

# 3. Highest-Utilization / Idle-Time-Based Matching Driver Matching Strategy

#     -Prioritize drivers who have been idle the longest.

#     -Balances driver earnings and avoids leaving some drivers without trips.

# 4. Surge Pricing / Revenue Maximization Driver Matching Strategy

#     -Match based on maximizing revenue for the platform (driver with higher surge zone, or rider willing to pay more).

#     -Useful in peak hours but may be perceived as unfair by riders.

# 5. Batch Matching (Auction / Marketplace Model) Driver Matching Strategy

#     -Instead of instant matching, the system waits a few seconds, collects multiple ride requests, and matches them with available drivers using:

#     -Hungarian Algorithm (min-cost bipartite matching).

#     -Optimization for minimum total wait time or maximum overall efficiency.

#     -Uber’s “dispatch waves” sometimes use this.

# 6. Driver Preference–Based Matching Driver Matching Strategy

#     -Some systems consider driver preferences (e.g., destination, trip length, rider rating).

#     -Example: A driver heading towards home is matched with riders going in that direction (“Driver Destination Mode”).

# 7. Rider Preference–Based Matching Driver Matching Strategy

#     -Riders may want specific types of drivers (highly rated, premium car, female driver, etc.).

#     -Matching accounts for these preferences alongside availability.

# 8. Pooling / Shared Ride Optimization Driver Matching Strategy

#     -For shared rides, the system matches riders not just with the nearest driver but also with other riders going in a similar direction.

#     -Optimized for minimizing detours and maximizing vehicle occupancy.

# 9. Fairness / Rotation-Based Matching Driver Matching Strategy

#     -Rotate assignments to ensure equitable distribution of rides among drivers.

#     -Prevents "winner-takes-all" situations where only drivers in dense areas get trips.

# 10. Wait-Time Minimization for Riders Driver Matching Strategy

#     -Instead of driver pickup distance, focus on reducing estimated wait time (taking into account traffic, driver’s route, etc.).

# 11. Hybrid / Weighted Scoring System Driver Matching Strategy

#     -Combine multiple factors (distance, driver idle time, rating, surge, rider preferences) into a scoring function:

#     -score = w1 * (pickup_distance)
#           + w2 * (driver_idle_time)
#           + w3 * (driver_rating)
#       + w4 * (rider_surge_zone) ...


#     -Match with the driver that maximizes/minimizes the score.


# FOR Simplification Now will only implement the Nearest Driver Matching Strategy

from abc import ABC, abstractmethod
from app.models.driver import Driver
from app.models.location import Location
from app.models.enums import RideType, DriverStatus


class DriverMatchingStrategy(ABC):
    @abstractmethod
    def get_available_drivers(self, all_drivers: list[Driver], pickup_location: Location, ride_type: RideType) -> list[Driver]:
        raise NotImplementedError("Subclasses must implement this method")


class NearestDriverMatchingStrategy(DriverMatchingStrategy):
    def __init__(self, max_distance: float = 5.0):
        # Max distance to consider a driver "nearby" for the ride request
        self.max_distance_criteria_for_nearby_drivers = max_distance

    def get_available_drivers(self, all_drivers: list[Driver], pickup_location: Location, ride_type: RideType) -> list[Driver]:
        print(f"Finding nearest drivers for ride type: {ride_type.value}")
        available_drivers = [
            driver
            for driver in all_drivers
            if driver.get_status() == DriverStatus.AVAILABLE
            and driver.get_vehicle_type() == ride_type.get_vehicle_type()
            and driver.get_current_location().to_distance(pickup_location) <= self.max_distance_criteria_for_nearby_drivers
        ]
        return sorted(available_drivers, key=lambda driver: driver.get_current_location().to_distance(pickup_location))
