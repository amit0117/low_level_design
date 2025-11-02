from abc import ABC, abstractmethod
from app.models.vehicle import Vehicle
from app.models.parking_spot import ParkingSpot
import random

# There are several parking spot assignment strategies that can be implemented for a parking lot.
# 1. Nearest Spot Assignment Strategy
#     - Assign the nearest spot to the vehicle.
#     - Example: "The nearest spot is assigned to the vehicle."
# 2. First Come First Serve Spot Assignment Strategy
#     - Assign the first available spot to the vehicle.
#     - Example: "The first available spot is assigned to the vehicle."
# 3. Random Spot Assignment Strategy
#     - Assign a random spot to the vehicle.
#     - Example: "A random spot is assigned to the vehicle."
# 4. Zone Based Spot Assignment Strategy
#     - Parking lot has been divided into several zones like (A, B, C, D etc) Assign the spot based on the zone of the vehicle.
#     - Example: "The spot is assigned based on the zone of the vehicle."
# 5. Preferred by User Spot Assignment Strategy
#     - Assign the spot based on the preferred spot of the user.
#     - Example: "The spot is assigned based on the preferred spot of the user. like for person with disability
#     - electric vehicle needing charging spot, etc.


class ParkingSpotAssignmentStrategy(ABC):
    @abstractmethod
    def assign_parking_spot(self, available_spots: dict[int, list[ParkingSpot]], vehicle: Vehicle) -> tuple[int, ParkingSpot]:
        raise NotImplementedError("Subclasses must implement this method")


# For now only implement random spot assignment strategy


class RandomSpotAssignmentStrategy(ParkingSpotAssignmentStrategy):
    def assign_parking_spot(self, available_spots: dict[int, list[ParkingSpot]], vehicle: Vehicle) -> tuple[int, ParkingSpot]:
        if len(available_spots) == 0:
            return None, None
        floor_number = random.choice(list(available_spots.keys()))
        spot = random.choice(available_spots[floor_number])
        return floor_number, spot
