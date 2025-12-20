from enum import Enum


# This will also show the current color of the traffic light
class TrafficLightStatus(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


# Road directions at intersection
class Direction(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


# Signal phase types defining which roads can be green simultaneously
class PhaseType(Enum):
    NORTH_SOUTH_GREEN = "NORTH_SOUTH_GREEN"  # North and South roads green
    EAST_WEST_GREEN = "EAST_WEST_GREEN"  # East and West roads green
    ALL_RED = "ALL_RED"  # All roads red (transition phase)
    EMERGENCY_PHASE = "EMERGENCY_PHASE"  # Emergency vehicle priority (for future use)
