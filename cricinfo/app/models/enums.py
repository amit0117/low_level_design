from enum import Enum


class ExtraType(Enum):
    WIDE = "WIDE"
    NO_BALL = "NO_BALL"
    BYE = "BYE"
    LEG_BYE = "LEG_BYE"


class MatchType(Enum):
    T20 = ("T20", 2, 20)
    ODI = ("ODI", 2, 50)
    TEST = ("TEST", 4, 90)

    def __init__(self, name: str, total_innings: int, total_overs_per_innings: int):
        self._name = name
        self._total_innings = total_innings
        self._total_overs_per_innings = total_overs_per_innings

    @property
    def name(self) -> str:
        return self._name

    @property
    def total_innings(self) -> int:
        return self._total_innings

    @property
    def total_overs_per_innings(self) -> int:
        return self._total_overs_per_innings


class WicketType(Enum):
    BOWLED = "BOWLED"
    CAUGHT = "CAUGHT"
    LBW = "LBW"
    RUN_OUT = "RUN_OUT"
    STUMPED = "STUMPED"
    HIT_WICKET = "HIT_WICKET"


class MatchStatus(Enum):
    SCHEDULED = "SCHEDULED"
    LIVE = "LIVE"
    IN_BREAK = "IN_BREAK"
    FINISHED = "FINISHED"
    ABANDONED = "ABANDONED"


class PlayerRole(Enum):
    BATSMAN = "BATSMAN"
    BOWLER = "BOWLER"
    ALL_ROUNDER = "ALL_ROUNDER"
    WICKET_KEEPER = "WICKET_KEEPER"
