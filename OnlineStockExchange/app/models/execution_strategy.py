from app.models.enums import OrderType, TransactionType
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order


class ExecutionStrategy(ABC):
    @abstractmethod
    def can_execute(self, order: "Order") -> bool:
        raise NotImplementedError("Execution strategy not implemented")


class LimitOrder(ExecutionStrategy):

    def can_execute(self, order: "Order") -> bool:
        market_price = order.get_stock().get_price()
        # Market orders can be executed immediately if there are matching orders
        if order.transaction_type == TransactionType.BUY:
            # Buy only if market price is less than or equal to order price
            return market_price <= order.limit_price
        else:
            # Sell only if market price is greater than or equal to order price
            return market_price >= order.limit_price


class MarketOrder(ExecutionStrategy):

    def can_execute(self, order: "Order") -> bool:
        # Market orders can be executed immediately irrespective of market price
        return True


class StopLossOrder(ExecutionStrategy):

    def can_execute(order: "Order") -> bool:
        market_price = order.get_stock().get_price()
        # Only execute if market price go above or below the stop price
        if order.transaction_type == TransactionType.BUY:
            return order.stop_price >= market_price
        return order.stop_price <= market_price


class StopLimitOrder(ExecutionStrategy):

    def can_execute(self, order: "Order") -> bool:
        # If order has not triggered yet it will behave like stop order
        # Once triggered, act like a limit order
        # Altogether we can say for BUY the market price should be: stop_price<=market_price<=limit_price
        # and just opposite will be true for SELL order i.e market_price should be less(or equal to) than stop price but greater(or equal to) than limit price
        market_price = order.get_stock().get_price()
        if order.transaction_type == TransactionType.BUY:
            return (
                order.stop_price <= market_price and market_price <= order.limit_price
            )
        else:
            return (
                market_price <= order.stop_price and market_price >= order.limit_price
            )
