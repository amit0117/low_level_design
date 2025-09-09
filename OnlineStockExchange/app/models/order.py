# app/models/order.py
from app.models.enums import OrderType, TransactionType, OrderStatus
from app.models.execution_strategy import (
    ExecutionStrategy,
    MarketOrder,
    LimitOrder,
    StopLossOrder,
    StopLimitOrder,
)
from app.models.stock import Stock
from app.models.order_state import OrderState, OpenState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Order:
    def __init__(
        self,
        order_id: str,
        order_type: OrderType,
        transaction_type: TransactionType,
        quantity: int,
        strategy: ExecutionStrategy,
        stock: Stock,
        user: "User",
    ):
        self.order_id = order_id
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.strategy = strategy
        self.state = OpenState()
        self.status = OrderStatus.OPEN
        self.stock = stock
        self.user = user

    def get_quantity(self) -> int:
        return self.quantity

    def get_user(self) -> "User":
        return self.user

    def get_stock(self) -> Stock:
        return self.stock

    def get_type(self) -> OrderType:
        return self.order_type

    def get_status(self) -> OrderStatus:
        return self.status

    def get_state(self) -> OrderState:
        return self.state

    def set_state(self, state: OrderState):
        self.state = state

    def set_status(self, status: OrderStatus):
        self.status = status

    def cancel(self):
        self.state.cancel(self)

    def can_execute(self, market_price: float):
        return self.strategy.can_execute(self, market_price)


class OrderBuilder:
    def __init__(self, order_id, order_type, transaction_type, quantity, stock, user):
        self.order_id = order_id
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.stock = stock
        self.user = user
        self.strategy = None

    def as_market(self):
        self.strategy = MarketOrder()
        return self

    def as_limit(self, limit_price: float):
        self.limit_price = limit_price
        self.strategy = LimitOrder()
        return self

    def as_stop_loss(self, stop_price: float):
        self.stop_price = stop_price
        self.strategy = StopLossOrder
        return self

    def as_stop_limit(self, stop_price: float, limit_price: float):
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.strategy = StopLimitOrder()
        return self

    def _is_valid(self):
        if not self.strategy:
            raise ValueError("No Execution strategy has been selected for this role")

        if (
            (self.strategy == LimitOrder and not self.limit_price)
            or (self.strategy == StopLossOrder and not self.stop_price)
            or (
                self.strategy == StopLimitOrder
                and not any(self.limit_price or self.stop_price)
            )
        ):
            raise ValueError("Invalid request")

    def build(self) -> Order:
        if not self.strategy:
            raise ValueError("Execution strategy must be set before building the order")

        return Order(
            self.order_id,
            self.order_type,
            self.transaction_type,
            self.quantity,
            self.strategy,
            self.stock,
            self.user,
        )
