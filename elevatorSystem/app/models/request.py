from app.models.enums import Direction, RequestType
from dataclasses import dataclass


@dataclass
class Request:
    target_floor_number: int
    direction: Direction
    type: RequestType

    def __str__(self):
        if self.type == RequestType.EXTERNAL:
            return f"{self.type.value} Request to floor {self.target_floor_number} going {self.direction.value}"
        else:
            return f"{self.type.value} Request to floor {self.target_floor_number}"

    def __hash__(self):
        return hash((self.target_floor_number, self.direction, self.type))

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.target_floor_number == other.target_floor_number and self.direction == other.direction and self.type == other.type
