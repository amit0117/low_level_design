from enum import Enum


class DoorStatus(Enum):
    OPENED = "opened"
    CLOSED = "closed"


class ElevatorStatus(Enum):
    IDLE = "idle"
    MOVING = "moving"
    IN_MAINTENANCE = "in_maintenance"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    IDLE = "idle"


class RequestType(Enum):
    INTERNAL = "internal"  # From inside the cabin
    EXTERNAL = "external"  # From the hall/floor
