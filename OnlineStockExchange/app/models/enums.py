from enum import Enum


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(Enum):
    OPEN = "OPEN"
    TRIGGERED = "TRIGGERED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    FILLED = "FILLED"
    FAILED = "FAILED"
