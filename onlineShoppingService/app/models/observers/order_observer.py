# This is to update the order status (like if order is placed, shipped, delivered, cancelled, returned)
# TO customer service purpose, admin purpose (For analytics), warehouse purpose (For inventory management, Shipping and delivery)
from abc import ABC, abstractmethod
from app.models.enums import OrderStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order


class OrderObserver(ABC):
    @abstractmethod
    def update_about_order(self, order: "Order"):
        raise NotImplementedError("Subclass must implement this method")


class CustomerOrderObserver(OrderObserver):
    def update_about_order(self, order: "Order"):
        # Update in all cases
        print(f"Customer received update about order {order}")


class AdminOrderObserver(OrderObserver):
    def update_about_order(self, order: "Order"):
        # only notify if status is shipped, delivered, cancelled, returned
        if order.get_status() in [OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED, OrderStatus.RETURNED]:
            print(f"Admin dashboard updated about order {order}")


class WarehouseOrderObserver(OrderObserver):
    def update_about_order(self, order: "Order"):
        if order.get_status() == OrderStatus.SHIPPED:
            print(f"Warehouse received update about order {order}")


class OrderSubject:
    def __init__(self) -> None:
        self.observers: list[OrderObserver] = []

    def add_observer(self, observer: OrderObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: OrderObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, order: "Order") -> None:
        for observer in self.observers:
            observer.update_about_order(order)
