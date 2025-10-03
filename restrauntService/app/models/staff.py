from app.models.enums import StaffRole
from app.observers.order_observer import OrderObserver
from app.observers.inventory_observer import InventoryObserver
from app.models.item import Item
from app.models.order_item import OrderItem


class Staff:
    def __init__(self, name: str, role: StaffRole) -> None:
        self.name = name
        self.role = role

    def get_name(self) -> str:
        return self.name

    def get_role(self) -> StaffRole:
        return self.role


class Waiter(Staff, OrderObserver):
    def __init__(self, name: str) -> None:
        super().__init__(name, StaffRole.WAITER)

    def serve_order(self, order_item: OrderItem) -> None:
        print(f"Waiter {self.name} is serving order item {order_item.get_item().get_name()}")

    def update_order_status(self, order_item: OrderItem) -> None:
        print(f"Waiter {self.name} is notified that order item {order_item.get_item().get_name()} is ready for pickup")


class Chef(Staff):
    def __init__(self, name: str) -> None:
        super().__init__(name, StaffRole.CHEF)

    def prepare_order(self, order_item: OrderItem) -> None:
        print(f"Chef {self.name} is preparing order item {order_item.get_item().get_name()}")


class Manager(Staff, InventoryObserver):
    def __init__(self, name: str) -> None:
        super().__init__(name, StaffRole.MANAGER)

    def update_inventory_status(self, item: Item, quantity: int) -> None:
        print(f"Notification for Manager:")
