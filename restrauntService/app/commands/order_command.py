from app.models.order_item import OrderItem
from abc import ABC, abstractmethod
from app.models.staff import Waiter, Chef


class OrderCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class ServeOrderCommand(OrderCommand):
    def __init__(self, order_item: OrderItem, waiter: Waiter) -> None:
        self.order_item = order_item
        self.waiter = waiter

    def execute(self) -> None:
        self.waiter.serve_order(self.order_item)
        self.order_item.serve_item()


class PrepareOrderCommand(OrderCommand):
    def __init__(self, order_item: OrderItem, chef: Chef) -> None:
        self.order_item = order_item
        self.chef = chef

    def execute(self) -> None:
        self.chef.prepare_order(self.order_item)
        self.order_item.start_preparation()
