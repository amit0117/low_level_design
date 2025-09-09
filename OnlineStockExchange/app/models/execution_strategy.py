from app.models.enums import OrderType, TransactionType
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order


class ExecutionStrategy(ABC):
    @abstractmethod
    def can_execute(self, order: "Order", market_price: float) -> bool:
        raise NotImplementedError("Execution strategy not implemented")


class LimitOrder(ExecutionStrategy):

    def can_execute(self, order: "Order", market_price: float) -> bool:
        # Market orders can be executed immediately if there are matching orders
        if order.transaction_type == TransactionType.BUY:
            # Buy only if market price is less than or equal to order price
            return market_price <= order.limit_price
        else:
            # Sell only if market price is greater than or equal to order price
            return market_price >= order.limit_price


class MarketOrder(ExecutionStrategy):
    def can_execute(self, order: "Order", market_price: float) -> bool:
        # Market orders can be executed immediately at current market price
        return True


class StopLossOrder(ExecutionStrategy):
    def can_execute(order: "Order", market_price: float) -> bool:
        # Only execute if market price go above or below the stop price
        if order.transaction_type == TransactionType.BUY:
            return order.stop_price >= market_price
        return order.stop_price <= market_price


class StopLimitOrder(ExecutionStrategy):
    def __init__(self, has_triggered: bool = False):
        self.has_triggered = has_triggered

    def can_execute(self, order: "Order", market_price: float) -> bool:
        # If order has not triggered yet it will behave like stop order
        if not self.has_triggered:
            if (
                order.transaction_type == TransactionType.BUY
                and market_price >= order.stop_price
            ) or (
                order.transaction_type == TransactionType.SELL
                and market_price <= order.stop_price
            ):
                return True

        # Once triggered, act like a limit order
        if self.has_triggered:
            if (
                order.transaction_type == TransactionType.BUY
                and order.limit_price <= market_price
            ) or (
                order.transaction_type == TransactionType.SELL
                and market_price >= order.limit_price
            ):
                return True

        # Return False in all other cases
        return False
