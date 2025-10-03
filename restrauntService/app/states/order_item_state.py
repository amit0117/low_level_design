from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.exceptions.state_transition import InvalidStateTransition
from app.models.enums import OrderItemStatus

if TYPE_CHECKING:
    from app.models.order_item import OrderItem


class OrderItemState(ABC):
    @abstractmethod
    def start_preparation(self, order_item: "OrderItem") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def serve_item(self, order_item: "OrderItem") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def cancel_order_item(self, order_item: "OrderItem") -> None:
        raise NotImplementedError("Subclasses must implement this method")


class OrderedState(OrderItemState):
    def start_preparation(self, order_item: "OrderItem") -> None:
        order_item.set_status(OrderItemStatus.PREPARING)
        order_item.set_state(PreparingState())

    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition("Cannot make a ready for pickup an ordered item")

    def cancel_order_item(self, order_item: "OrderItem") -> None:
        print(f"Cancelling order item {order_item.get_item().get_name()}")
        order_item.set_status(OrderItemStatus.CANCELLED)
        order_item.set_state(CancelledState())

    def serve_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition("Cannot serve an ordered item")


class PreparingState(OrderItemState):
    def start_preparation(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already preparing, cannot re-start preparation again")

    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        print(f"Making ready for pickup item {order_item.get_item().get_name()}")
        order_item.set_status(OrderItemStatus.READY_FOR_PICKUP)
        order_item.set_state(ReadyForPickupState())

    def cancel_order_item(self, order_item: "OrderItem") -> None:
        print(f"Cancelling order item {order_item.get_item().get_name()}")
        order_item.set_status(OrderItemStatus.CANCELLED)
        order_item.set_state(CancelledState())

    def serve_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition("Cannot serve an preparing item")


class ReadyForPickupState(OrderItemState):
    def start_preparation(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition("Cannot start preparation an already ready for pickup item")

    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition("Cannot make a ready for pickup an already ready for pickup item")

    def cancel_order_item(self, order_item: "OrderItem") -> None:
        print(f"Cancelling order item {order_item.get_item().get_name()}")
        order_item.set_status(OrderItemStatus.CANCELLED)
        order_item.set_state(CancelledState())

    def serve_item(self, order_item: "OrderItem") -> None:
        order_item.set_status(OrderItemStatus.SERVED)
        order_item.set_state(ServedState())


class ServedState(OrderItemState):
    def start_preparation(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already served, cannot start preparation again")

    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already served, cannot make ready for pickup again")

    def cancel_order_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already served, cannot cancel again")

    def serve_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already served, cannot serve again")


class CancelledState(OrderItemState):
    def start_preparation(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already cancelled, cannot start preparation again")

    def make_ready_for_pickup(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already cancelled, cannot make ready for pickup again")

    def cancel_order_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already cancelled, cannot cancel again")

    def serve_item(self, order_item: "OrderItem") -> None:
        raise InvalidStateTransition(f"item:{order_item.get_item().get_name()} is already cancelled, cannot serve again")
