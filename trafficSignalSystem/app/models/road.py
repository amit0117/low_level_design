from typing import TYPE_CHECKING, Optional
from app.models.enums import Direction

if TYPE_CHECKING:
    from app.models.traffic_light import TrafficLight


class Road:
    def __init__(self, road_id: str, direction: Direction, num_lanes: int = 2):
        self.road_id = road_id
        self.direction = direction
        self.num_lanes = num_lanes
        self._traffic_light: Optional["TrafficLight"] = None

    def set_traffic_light(self, traffic_light: "TrafficLight") -> None:
        self._traffic_light = traffic_light

    def get_traffic_light(self) -> Optional["TrafficLight"]:
        return self._traffic_light

    def get_direction(self) -> Direction:
        return self.direction

    def __repr__(self) -> str:
        return f"Road(id={self.road_id}, direction={self.direction.value}, lanes={self.num_lanes})"
