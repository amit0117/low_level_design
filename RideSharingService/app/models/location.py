import math


class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def to_distance(self, other: "Location") -> float:
        dx = self.latitude - other.get_latitude()
        dy = self.longitude - other.get_longitude()
        return math.sqrt(dx * dx + dy * dy)  # For simplicity, we are using Euclidean formula to calculate the distance between two points.

    def __str__(self) -> str:
        return f"Location({self.get_latitude()}, {self.get_longitude()})"
