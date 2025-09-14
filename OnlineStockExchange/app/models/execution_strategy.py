from app.models.enums import TransactionType, OrderStatus
from app.models.order_state import TriggerState
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

    def can_execute(self, order: "Order") -> bool:
        market_price = order.get_stock().get_price()

        if not getattr(order, "has_triggered", False):  # not triggered yet
            if (
                order.transaction_type == TransactionType.BUY
                and market_price >= order.get_stop_price()
            ):
                # change the state and status of order
                order.set_state(TriggerState())
                order.set_status(OrderStatus.TRIGGERED)
                order.has_triggered = True
                # Once Triggered , order will act as a Market Order
                return True
            elif (
                order.transaction_type == TransactionType.SELL
                and market_price <= order.get_stop_price()
            ):
                # change the state and status of order
                order.set_state(TriggerState())
                order.set_status(OrderStatus.TRIGGERED)
                order.has_triggered = True
                return True
            return False  # not executed yet, only waiting

        # Once triggered, behave like a MarketOrder
        return True


class StopLimitOrder(ExecutionStrategy):
    def can_execute(self, order: "Order") -> bool:
        market_price = order.get_stock().get_price()

        if not getattr(order, "has_triggered", False):  # waiting
            if (
                order.transaction_type == TransactionType.BUY
                and market_price >= order.get_stop_price()
            ):
                # change the state and status of order
                order.set_state(TriggerState())
                order.set_status(OrderStatus.TRIGGERED)
                order.has_triggered = True
            elif (
                order.transaction_type == TransactionType.SELL
                and market_price <= order.get_stop_price()
            ):
                # change the state and status of order
                order.set_state(TriggerState())
                order.set_status(OrderStatus.TRIGGERED)
                order.has_triggered = True
            else:
                # If not triggered and does not meet any criteria for triggering then return false
                return False

        # Once triggered, behave like a LimitOrder
        if order.transaction_type == TransactionType.BUY:
            return market_price <= order.limit_price
        else:
            return market_price >= order.limit_price
