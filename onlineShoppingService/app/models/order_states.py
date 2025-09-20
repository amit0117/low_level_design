from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.models.enums import OrderStatus

if TYPE_CHECKING:
    from app.models.order import Order


class OrderState(ABC):
    @abstractmethod
    def place(self, order: "Order") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def ship(self, order: "Order") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def deliver(self, order: "Order") -> None:
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def cancel(self, order: "Order") -> None:
        raise NotImplementedError("Subclass must implement this method")


class PendingState(OrderState):
    def place(self, order: "Order") -> None:
        print("Order is in pending state, cannot place. please pay first")

    def ship(self, order: "Order") -> None:
        print("Order is in pending state, cannot ship. please pay first")

    def deliver(self, order: "Order") -> None:
        print("Order is in pending state, cannot deliver. please pay first")

    def cancel(self, order: "Order") -> None:
        print("Order is in pending state, cannot cancel. please pay first")


class PlacedState(OrderState):
    def place(self, order: "Order") -> None:
        print("Order is already placed.")

    def ship(self, order: "Order") -> None:
        print(f"Shipping order to customer,{order.get_owner().get_user_name()} to shipping address,{str(order.get_owner().get_shipping_address())}")
        order.set_status(OrderStatus.SHIPPED)
        order.set_state(ShippedState())

    def deliver(self, order: "Order") -> None:
        print("Cannot deliver an order that has not been shipped.")

    def cancel(self, order: "Order") -> None:
        print(f"Cancelling order {order.get_order_id()}")
        order.set_status(OrderStatus.CANCELLED)
        order.set_state(CancelledState())


class ShippedState(OrderState):
    def place(self, order: "Order") -> None:
        print("Order is already shipped.")

    def ship(self, order: "Order") -> None:
        print("Order is already shipped.")

    def deliver(self, order: "Order") -> None:
        print(
            f"Delivering order {order.get_order_id()} to customer,{order.get_owner().get_user_name()} to shipping address,{str(order.get_owner().get_shipping_address())}"
        )
        order.set_status(OrderStatus.DELIVERED)
        order.set_state(DeliveredState())

    def cancel(self, order: "Order") -> None:
        print("Cannot cancel a shipped order.")


class DeliveredState(OrderState):
    def place(self, order: "Order") -> None:
        print("Order is already delivered.")

    def ship(self, order: "Order") -> None:
        print("This order is already delivered. cannot ship it again.")

    def deliver(self, order: "Order") -> None:
        print("This order is already delivered. cannot deliver it again.")

    def cancel(self, order: "Order") -> None:
        print("This order is already delivered. cannot cancel it.")


class CancelledState(OrderState):
    def place(self, order: "Order") -> None:
        print("This order has already cancelled.")

    def ship(self, order: "Order") -> None:
        print("Cannot ship a cancelled order.")

    def deliver(self, order: "Order") -> None:
        print("Cannot deliver a cancelled order.")

    def cancel(self, order: "Order") -> None:
        print("This order has already cancelled.")


class ReturnedState(OrderState):
    def place(self, order: "Order") -> None:
        print("This order has already returned.")

    def ship(self, order: "Order") -> None:
        print("Cannot ship a returned order.")

    def deliver(self, order: "Order") -> None:
        print("Cannot deliver a returned order.")

    def cancel(self, order: "Order") -> None:
        print("This order has already returned.")
