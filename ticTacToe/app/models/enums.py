from enum import Enum


class GameStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class PlayerSymbol(Enum):
    X = "X"
    O = "O"


class PlayerType(Enum):
    HUMAN = "HUMAN"
    COMPUTER = "COMPUTER"
