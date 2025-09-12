from threading import Lock
from typing import Optional
from app.models.order import Order
from app.models.enums import OrderStatus, OrderType
from collections import defaultdict
from app.exceptions import NoMatchStockFoundException

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
        with self.match_lock:
            self.buy_orders[order.get_stock().get_symbol()].append(order)
            self._match_order(order.get_stock())

    def play_sell_order(self, order: Order) -> None:
        with self.match_lock:
            self.sell_orders(order.get_stock().get_symbol()).append(order)
            self._match_order(order.get_stock())

    def _find_best_buy_order(self, buy_orders: list[Order]) -> Order:
        # Only check for Open Order and have some quantity left for trading
        available_buy_order_without_market_order = [
            o
            for o in buy_orders
            if o.get_status() == OrderStatus.OPEN.value
            and o.can_execute()
            and o.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]
        ]

        # Ideally stock exchange follows price/time priority order
        # For market order we can place the buy order to any matching sell order
        # For simplification we ignoring time while matching order
        if available_buy_order_without_market_order:
            return max(
                available_buy_order_without_market_order,
                # For market and Stop Loss if they are executable they become market order and that can be sold at any price
                key=lambda o: o.get_stop_price(),
            )
        print("No limit order found for buy")
        # Check if there is at least one market or stop loss order,if executable both market and stop loss can be buy at any price
        for order in buy_orders:
            if (
                order not in available_buy_order_without_market_order
                and order.can_execute()
            ):
                return order
        print("no buy order found. Raising Exception")
        raise NoMatchStockFoundException()

    def _find_best_sell_order(self, sell_orders: list[Order]) -> Order:
        available_sell_order_without_limit = [
            o
            for o in sell_orders
            if o.get_status() == OrderStatus.OPEN
            and o.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]
        ]
        if available_sell_order_without_limit:
            return min(
                available_sell_order_without_limit, key=lambda o: o.get_stop_price()
            )
        print("No limit order found for sell")
        for order in sell_orders:
            if order not in available_sell_order_without_limit and order.can_execute():
                return order
        print("No relevant sell order found. Raising exception")

        raise NoMatchStockFoundException()

    def _match_order(self, order: Order) -> None:
        pass
