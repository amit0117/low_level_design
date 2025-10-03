from typing import List, Optional
import uuid
from app.repositories.order_repository import OrderRepository
from app.repositories.table_repository import TableRepository
from app.repositories.menu_repository import MenuRepository
from app.repositories.inventory_repository import InventoryRepository
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.models.staff import Chef, Waiter
from app.commands.order_command import PrepareOrderCommand, ServeOrderCommand
from app.exceptions.inventory import InsufficientStockException
from app.exceptions.item import MissingItemException


class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.table_repo = TableRepository()
        self.menu_repo = MenuRepository()
        self.inventory_repo = InventoryRepository()

    def create_order(self, table_number: int, customer_name: str, item_orders: List[OrderItem]) -> Optional[Order]:

        # Business validation
        table = self.table_repo.find_by_id(table_number)
        if not table or not table.is_occupied():
            print(f"Table {table_number} not found or not occupied")
            return None

        # Business workflow
        order_items = []
        order_id = str(uuid.uuid4())
        customer = Customer(customer_name)

        for item_order in item_orders:
            item_name = item_order.get_item().get_name()
            quantity = item_order.get_quantity()

            # Business validation - check menu
            menu_item = self.menu_repo.find_item_by_name(item_name)
            if not menu_item:
                raise MissingItemException(f"Item {item_name} not found in menu")

            # Business validation - check inventory
            if self.inventory_repo.find_item_quantity(menu_item) < quantity:
                raise InsufficientStockException(f"Insufficient stock for {item_name}")

            # Create order item
            order_item = OrderItem(order_id, menu_item, quantity)
            order_items.append(order_item)

        # Business logic - create order
        order = Order(table_number, order_items, customer)
        self.order_repo.save(order)

        print(f"Order {order.get_order_id()} created for table {table_number}")
        return order

    def process_order(self, order_id: str, chef: Chef) -> bool:
        order = self.order_repo.find_by_id(order_id)

        if not order:
            print(f"Order {order_id} not found")
            return False

        # Business workflow
        for order_item in order.get_items():
            # Start preparation
            prepare_command = PrepareOrderCommand(order_item, chef)
            prepare_command.execute()

            # Update inventory
            self.inventory_repo.update_quantity(order_item.get_item(), -order_item.get_quantity())

        print(f"Order {order_id} is being prepared by chef {chef.get_name()}")
        return True

    def mark_order_items_ready(self, order_id: str) -> bool:
        order = self.order_repo.find_by_id(order_id)

        if not order:
            print(f"Order {order_id} not found")
            return False

        # Business workflow
        for order_item in order.get_items():
            order_item.make_ready_for_pickup()
            print(f"Order item {order_item.get_item().get_name()} is ready for pickup")

        return True

    def serve_order(self, order_id: str, waiter: Waiter) -> bool:
        order = self.order_repo.find_by_id(order_id)

        if not order or not waiter:
            print(f"Order {order_id} or waiter not found")
            return False

        # Business workflow
        for order_item in order.get_items():
            serve_command = ServeOrderCommand(order_item, waiter)
            serve_command.execute()

        print(f"Order {order_id} served by waiter {waiter.get_name()}")
        return True

    def get_all_orders(self) -> List[Order]:
        return self.order_repo.find_all()

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return self.order_repo.find_by_id(order_id)

    def get_order_status(self) -> dict:
        orders = self.order_repo.find_all()
        active_orders = self.order_repo.find_active_orders()

        return {"total": len(orders), "active": len(active_orders)}
