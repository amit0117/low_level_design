from __future__ import annotations
from app.utils import SingletonMeta
from threading import Lock
from app.models.order import Order
from app.models.stock import Stock
from app.models.order_state import PartiallyFilledState, FilledState, FailedState
from app.models.enums import OrderStatus, TransactionType
from collections import defaultdict
from app.exceptions import NoMatchStockFoundException


class StockExchange(metaclass=SingletonMeta):

    def __init__(self):
        # Order Book
        self.buy_orders: dict[str, list[Order]] = defaultdict(list)
        self.sell_orders: dict[str, list[Order]] = defaultdict(list)
        self.match_lock = Lock()

    def place_buy_order(self, order: Order) -> None:
        with self.match_lock:
            self.buy_orders[order.get_stock().get_symbol()].append(order)
            self._match_order(order.get_stock())

    def place_sell_order(self, order: Order) -> None:
        with self.match_lock:
            self.sell_orders[order.get_stock().get_symbol()].append(order)
            self._match_order(order.get_stock())

    def _find_best_buy_order(self, buy_orders: list[Order]) -> Order:
        executable_orders = [o for o in buy_orders if o.get_status() == OrderStatus.OPEN and o.can_execute()]

        if not executable_orders:
            raise NoMatchStockFoundException()

        # Market / stop-loss (market-like): immediate-execution intent — prioritize over resting limits (FIFO).
        limit_orders = [o for o in executable_orders if o.is_limit_like()]
        market_orders = [o for o in executable_orders if o.is_market_like()]

        if market_orders:
            return market_orders[0]
        if limit_orders:
            return max(limit_orders, key=lambda o: o.get_limit_price())

        raise NoMatchStockFoundException()

    def _find_best_sell_order(self, sell_orders: list[Order]) -> Order:
        executable_orders = [o for o in sell_orders if o.get_status() == OrderStatus.OPEN and o.can_execute()]

        if not executable_orders:
            raise NoMatchStockFoundException()

        # Market / stop-loss (market-like): immediate-execution intent — prioritize over resting limits (FIFO).
        limit_orders = [o for o in executable_orders if o.is_limit_like()]
        market_orders = [o for o in executable_orders if o.is_market_like()]

        if market_orders:
            return market_orders[0]
        if limit_orders:
            return min(limit_orders, key=lambda o: o.get_limit_price())

        raise NoMatchStockFoundException()

    def _match_order(self, stock: Stock) -> None:
        # Don't acquire lock here since it's already held by the calling method
        buys = self.buy_orders[stock.get_symbol()]
        sells = self.sell_orders[stock.get_symbol()]

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
        # For market orders, they can always match with each other
        if buy_order.is_market_like() and sell_order.is_market_like():
            return True

        # For limit orders, check price compatibility
        buy_price = self._get_execution_price(buy_order)
        sell_price = self._get_execution_price(sell_order)

        return buy_price >= sell_price

    def _get_execution_price(self, order: Order) -> float:
        if order.is_limit_like():
            return order.get_limit_price()
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
        # If both are market orders, use current stock price
        if all(order.is_market_like() for order in [buy_order, sell_order]):
            return buy_order.get_stock().get_price()

        # check if both are limit orders (why this works because of the buy_price >= sell_price condition we have in the _can_match method)
        if all(order.is_limit_like() for order in [buy_order, sell_order]):
            return min(buy_order.get_limit_price(), sell_order.get_limit_price())

        # One market-like, one limit-like: print at the resting limit (market has no limit price)
        if buy_order.is_limit_like():
            return buy_order.get_limit_price()
        return sell_order.get_limit_price()

    def _check_stop_orders_after_price_change(self, stock: Stock) -> None:
        """Check and trigger stop orders after stock price changes"""
        symbol = stock.get_symbol()

        # Check buy stop orders
        for order in self.buy_orders[symbol]:
            if order.is_stop_like():
                if order.get_status() == OrderStatus.OPEN and order.can_execute():
                    # Order got triggered, try to match again
                    self._match_order(stock)
                    break

        # Check sell stop orders
        for order in self.sell_orders[symbol]:
            if order.is_stop_like():
                if order.get_status() == OrderStatus.OPEN and order.can_execute():
                    # Order got triggered, try to match again
                    self._match_order(stock)
                    break

    def _execute_partial(self, order: Order, quantity: int, price: float) -> None:
        try:
            # Handle account changes
            account = order.get_owner().get_account()
            total_amount = quantity * price

            if order.transaction_type == TransactionType.BUY:
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
                # remove from order book
                if order.transaction_type == TransactionType.BUY:
                    self.buy_orders[order.get_stock().get_symbol()].remove(order)
                else:
                    self.sell_orders[order.get_stock().get_symbol()].remove(order)
            else:
                order.set_state(PartiallyFilledState())
                order.set_status(OrderStatus.PARTIALLY_FILLED)
                order.set_quantity(remaining_quantity)

        except Exception as e:
            order.set_state(FailedState())
            order.set_status(OrderStatus.FAILED)
            print(f"Error executing trade: {e}")
