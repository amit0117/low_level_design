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
from typing import TYPE_CHECKING, Optional
from uuid import uuid4
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User


class Order:

    def __init__(
        self,
        order_id: str,
        ordered_at: datetime,
        order_type: OrderType,
        transaction_type: TransactionType,
        quantity: int,
        strategy: ExecutionStrategy,
        stock: Stock,
        user: "User",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ):
        self.order_id = order_id
        self.ordered_at = ordered_at
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.strategy = strategy
        self.state = OpenState()
        self.status = OrderStatus.OPEN
        self.stock = stock
        self.owner = user
        self.limit_price = limit_price
        self.stop_price = stop_price
        self.has_triggered = False  # Required for stop loss / stop limit order type

    def __repr__(self):
        print(
            f"order with order_type: {self.order_type}, quantity: {self.quantity} , limit_price :{self.limit_price}, stop_price: {self.stop_price}, transaction_type: {self.transaction_type}"
        )

    def get_quantity(self) -> int:
        return self.quantity

    def get_owner(self) -> "User":
        return self.owner

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

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def set_status(self, status: OrderStatus):
        self.status = status
        self._notify_owner()

    def get_limit_price(self) -> float:
        return self.limit_price

    def get_stop_price(self) -> float:
        return self.stop_price

    def cancel(self):
        self.state.cancel(self)

    def can_execute(self):
        return self.strategy.can_execute(self)

    def _notify_owner(self) -> None:
        if self.owner:
            self.owner.order_status_update(self)


class OrderBuilder:

    def __init__(self):
        self.reset()

    def reset(self):
        self.stock: Optional[Stock] = None
        self.user: Optional[User] = None
        self.order_type: Optional[OrderType] = None
        self.transaction_type: Optional[TransactionType] = None
        self.quantity: int = 0
        self.limit_price: float = 0.0
        self.stop_price: float = 0.0

    def for_user(self, user: User) -> "OrderBuilder":
        self.user = user
        return self

    def with_stock(self, stock: Stock) -> "OrderBuilder":
        self.stock = stock
        return self

    def sell(self, quantity: int) -> "OrderBuilder":
        self.transaction_type = TransactionType.SELL
        self.quantity = quantity
        return self

    def buy(self, quantity: int) -> "OrderBuilder":
        self.quantity = quantity
        self.transaction_type = TransactionType.BUY
        return self

    def as_market(self) -> "OrderBuilder":
        self.strategy = MarketOrder()
        return self

    def as_limit(self, limit_price: float) -> "OrderBuilder":
        self.limit_price = limit_price
        self.strategy = LimitOrder()
        return self

    def as_stop_loss(self, stop_price: float) -> "OrderBuilder":
        self.stop_price = stop_price
        self.strategy = StopLossOrder()
        return self

    def as_stop_limit(self, stop_price: float, limit_price: float) -> "OrderBuilder":
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.strategy = StopLimitOrder()
        return self

    def _is_valid(self) -> bool:
        if not self.strategy:
            return False

        if (
            (self.strategy == OrderType.LIMIT and not self.limit_price)
            or (self.strategy == OrderType.STOP_LOSS and not self.stop_price)
            or (
                self.strategy == OrderType.STOP_LIMIT
                and not any(self.limit_price or self.stop_price)
            )
        ):
            return False
        return True

    def build(self) -> Order:
        if not self._is_valid():
            raise ValueError("Execution strategy must be set before building the order")

        return Order(
            str(uuid4()),
            self.order_type,
            datetime.now(),
            self.transaction_type,
            self.quantity,
            self.strategy,
            self.stock,
            self.user,
            self.limit_price,
            self.stop_price,
        )
