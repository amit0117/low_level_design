from threading import Lock
from typing import Optional
from app.models.order import Order
from app.models.enums import OrderStatus
from collections import defaultdict


class StockExchange:
    _lock = Lock()
    _instance: Optional["StockExchange"] = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__()
        return cls._instance

    def __init__(self):
        if hasattr(self, "has_initialized"):
            return
        # Order Book
        self.buy_orders: dict[str, list[Order]] = defaultdict(list)
        self.sell_orders = dict[str, list[Order]] = defaultdict(list)
        self.match_lock = Lock()
        self.has_initialized = True

    @classmethod
    def get_instance(cls) -> "StockExchange":
        return cls()

    def place_buy_order(self, order: Order) -> None:
        self.buy_orders[order.get_stock().get_symbol()].append(order)
        self._match_order(order.get_stock())

    def play_sell_order(self, order: Order) -> None:
        self.sell_orders(order.get_stock().get_symbol()).append(order)
        self._match_order(order.get_stock())

    def _get_best_available_buy_order(self, buy_orders: list[Order]) -> Order:
        # Only check for Open Order and have some quantity left for trading
        available_buy_order = [
            o
            for o in buy_orders
            if o.get_status() == OrderStatus.OPEN.value
            and o.get_quantity > 0
            and o.can_execute()
        ]
        if not available_buy_order:
            return None

    def _match_order(self, order: Order) -> None:
        with self.match_lock:
            pass
