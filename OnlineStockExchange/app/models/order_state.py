from app.models.enums import OrderStatus
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order


class OrderState(ABC):
    @abstractmethod
    def cancel(self, order: "Order"):
        raise NotImplementedError("Cancel operation not allowed in current state")


class OpenState(OrderState):
    def cancel(self, order: "Order"):
        print("Cancelling opened order...:", order)
        order.set_status(OrderStatus.CANCELLED)
        order.set_state(CancelledState())


class TriggerState(OrderState):
    def cancel(self, order: "Order") -> None:
        print("Cancelling triggered order...", order)
        order.set_status(OrderStatus.CANCELLED)
        order.set_state(CancelledState())


class PartiallyFilledState(OrderState):
    def cancel(self, order: "Order"):
        print("Cancelling partially filled order... :", order)
        order.set_status(OrderStatus.CANCELLED)
        order.set_state(CancelledState())


class FilledState(OrderState):
    def cancel(self, order: "Order"):
        print("Order already filled with id:", order.order_id, " cannot cancel.")


class FailedState(OrderState):
    def cancel(self, order: "Order"):
        print("Order already failed with id:", order.order_id, " cannot cancel.")


class CancelledState(OrderState):
    def cancel(self, order: "Order"):
        print("Order already cancelled with id:", order.order_id)
