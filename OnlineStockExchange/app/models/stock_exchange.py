from threading import Lock
from typing import Optional
from app.models.order import Order
from app.models.stock import Stock
from app.models.order_state import (
    PartiallyFilledState,
    FilledState,
    FailedState,
)
from app.models.enums import OrderStatus, OrderType, TransactionType
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
        self.sell_orders: dict[str, list[Order]] = defaultdict(list)
        self.match_lock = Lock()
        self.has_initialized = True

    @classmethod
    def get_instance(cls) -> "StockExchange":
        return cls()

    def place_buy_order(self, order: Order) -> None:
        with self.match_lock:
            self.buy_orders[order.get_stock().get_symbol()].append(order)
            self._match_order(order.get_stock())

    def place_sell_order(self, order: Order) -> None:
        with self.match_lock:
            self.sell_orders[order.get_stock().get_symbol()].append(order)
            self._match_order(order.get_stock())

    def _find_best_buy_order(self, buy_orders: list[Order]) -> Order:
        executable_orders = [
            o
            for o in buy_orders
            if o.get_status() == OrderStatus.OPEN and o.can_execute()
        ]

        if not executable_orders:
            raise NoMatchStockFoundException()

        # Prioritize by order type and price
        limit_orders = [
            o
            for o in executable_orders
            if o.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]
        ]
        market_orders = [
            o
            for o in executable_orders
            if o.order_type in [OrderType.MARKET, OrderType.STOP_LOSS]
        ]

        if limit_orders:
            return max(limit_orders, key=lambda o: o.get_stop_price())
        elif market_orders:
            # IF there is any Market order (Market, Stop Limit order) that will always execute, So returning the first entry
            return market_orders[0]

        raise NoMatchStockFoundException()

    def _find_best_sell_order(self, sell_orders: list[Order]) -> Order:
        executable_orders = [
            o
            for o in sell_orders
            if o.get_status() == OrderStatus.OPEN and o.can_execute()
        ]

        if not executable_orders:
            raise NoMatchStockFoundException()

        # Prioritize by order type and price
        limit_orders = [
            o
            for o in executable_orders
            if o.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]
        ]
        market_orders = [
            o
            for o in executable_orders
            if o.order_type in [OrderType.MARKET, OrderType.STOP_LOSS]
        ]

        if limit_orders:
            return min(limit_orders, key=lambda o: o.get_stop_price())
        elif market_orders:
            # If there is any Market order (Market or Stop Limit) return because that will always execute
            return market_orders[0]

        raise NoMatchStockFoundException()

    def _match_order(self, stock: Stock) -> None:
        with self.match_lock:
            buys = self.buy_orders.get(stock.get_symbol(), [])
            sells = self.sell_orders.get(stock.get_symbol(), [])

            if not buys or not sells:
                return

            while True:
                try:
                    best_buy = self._find_best_buy_order(buys)
                    best_sell = self._find_best_sell_order(sells)

                    if self._can_match(best_buy, best_sell):
                        self._execute_trade(best_buy, best_sell)
                    else:
                        break

                except NoMatchStockFoundException:
                    break

    def _can_match(self, buy_order: Order, sell_order: Order) -> bool:
        buy_price = self._get_execution_price(buy_order)
        sell_price = self._get_execution_price(sell_order)
        return buy_price >= sell_price

    def _get_execution_price(self, order: Order) -> float:
        if order.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
            return order.get_stop_price()
        else:  # MARKET or STOP_LOSS
            return order.get_stock().get_price()

    def _execute_trade(self, buy_order: Order, sell_order: Order) -> None:
        # Determine execution price based on order types
        execution_price = self._determine_execution_price(buy_order, sell_order)

        # Calculate trade quantity
        trade_quantity = min(buy_order.get_quantity(), sell_order.get_quantity())

        # Update stock price to execution price
        buy_order.get_stock().set_price(execution_price)

        # Execute the trade
        self._execute_partial(buy_order, trade_quantity, execution_price)
        self._execute_partial(sell_order, trade_quantity, execution_price)

        # Check if price change triggers any stop orders
        self._check_stop_orders_after_price_change(buy_order.get_stock())

    def _determine_execution_price(self, buy_order: Order, sell_order: Order) -> float:
        # Market orders execute at the limit order price if available
        if buy_order.order_type in [OrderType.MARKET, OrderType.STOP_LOSS]:
            if sell_order.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
                return sell_order.get_stop_price()
        elif sell_order.order_type in [OrderType.MARKET, OrderType.STOP_LOSS]:
            if buy_order.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT]:
                return buy_order.get_stop_price()

        # Both are limit orders - use the better price for the market
        buy_price = buy_order.get_stop_price()
        sell_price = sell_order.get_stop_price()
        return min(buy_price, sell_price)

    def _check_stop_orders_after_price_change(self, stock: Stock) -> None:
        """Check and trigger stop orders after stock price changes"""
        symbol = stock.get_symbol()

        # Check buy stop orders
        for order in self.buy_orders.get(symbol, []):
            if order.order_type in [OrderType.STOP_LOSS, OrderType.STOP_LIMIT]:
                if order.get_status() == OrderStatus.OPEN and order.can_execute():
                    # Order got triggered, try to match again
                    self._match_order(stock)
                    break

        # Check sell stop orders
        for order in self.sell_orders.get(symbol, []):
            if order.order_type in [OrderType.STOP_LOSS, OrderType.STOP_LIMIT]:
                if order.get_status() == OrderStatus.OPEN and order.can_execute():
                    # Order got triggered, try to match again
                    self._match_order(stock)
                    break

    def _execute_partial(self, order: Order, quantity: int, price: float) -> None:
        try:
            # Handle account changes
            account = order.get_owner().get_account()
            total_amount = quantity * price

            if order.transaction_type.name == TransactionType.BUY:
                account.debit(total_amount)
                account.add_stock(order.get_stock().get_symbol(), quantity)
            else:  # SELL
                account.credit(total_amount)
                account.remove_stock(order.get_stock().get_symbol(), quantity)

            # Update order quantity and status
            remaining_quantity = order.get_quantity() - quantity
            if remaining_quantity == 0:
                order.set_state(FilledState())
                order.set_status(OrderStatus.FILLED)
            else:
                order.set_state(PartiallyFilledState())
                order.set_status(OrderStatus.PARTIALLY_FILLED)
                order.set_quantity(remaining_quantity)

        except Exception as e:
            order.set_state(FailedState())
            order.set_status(OrderStatus.FAILED)
            print(f"Error executing trade: {e}")
