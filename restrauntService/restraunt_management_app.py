import threading
from typing import List, Optional
import uuid
from app.models.menu import Menu
from app.models.inventory import Inventory
from app.models.staff import Manager, Chef, Waiter
from app.models.table import Table
from app.models.item import Item
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.customer import Customer
from app.commands.order_command import PrepareOrderCommand, ServeOrderCommand
from app.decorators.bill_decorator import TaxDecorator, ServiceChargeDecorator, DiscountDecorator
from app.strategies.payment_strategy import PaymentStrategy, Payment
from app.exceptions.inventory import InsufficientStockException
from app.exceptions.item import MissingItemException


class RestrauntManagementApp:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self.menu = Menu()
            self.inventory = Inventory()
            self.managers: List[Manager] = []
            self.chefs: List[Chef] = []
            self.waiters: List[Waiter] = []
            self.tables: List[Table] = []
            self.orders: List[Order] = []
            self.processing_lock = threading.Lock()
            self._initialized = True

    @classmethod
    def get_instance(cls) -> "RestrauntManagementApp":
        return cls()

    def add_manager(self, manager: Manager) -> None:
        self.managers.append(manager)

    def add_chef(self, chef: Chef) -> None:
        self.chefs.append(chef)

    def add_waiter(self, waiter: Waiter) -> None:
        self.waiters.append(waiter)

    def add_table(self, table: Table) -> None:
        self.tables.append(table)

    def get_available_tables(self) -> list[Table]:
        return [table for table in self.tables if table.is_available()]

    def get_menu(self) -> Menu:
        return self.menu

    def add_item_to_menu(self, item: Item) -> None:
        self.menu.add_item(item)

    def remove_item_from_menu(self, item: Item) -> None:
        self.menu.remove_item(item)

    def get_inventory(self) -> Inventory:
        return self.inventory

    def add_item_to_inventory(self, item: Item, quantity: int) -> None:
        self.inventory.add_item(item, quantity)

    def remove_item_from_inventory(self, item: Item, quantity: int) -> None:
        self.inventory.remove_item(item, quantity)

    def get_chefs(self) -> list[Chef]:
        return self.chefs

    def get_waiters(self) -> list[Waiter]:
        return self.waiters

    def get_managers(self) -> list[Manager]:
        return self.managers

    def get_tables(self) -> list[Table]:
        return self.tables

    def create_order(self, table: Table, order_items: list[OrderItem], ordered_by: str) -> Order:
        with self.processing_lock:
            order = Order(table.get_table_number(), order_items, ordered_by)
            self.orders.append(order)
            return order

    def get_orders(self) -> list[Order]:
        return self.orders

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return next((order for order in self.orders if order.get_order_id() == order_id), None)

    # Table Management
    def reserve_table(self, table_number: int, customer_name: str, size: int) -> bool:
        table = next((t for t in self.tables if t.get_table_number() == table_number), None)
        with self.processing_lock:
            if table and table.is_available() and size <= table.get_capacity():
                table.reserve_table()
                print(f"Table {table_number} reserved for {customer_name}")
                return True

        print(f"Table {table_number} not found or not available or size is too large")
        return False

    def occupy_table(self, table_number: int) -> bool:
        table = next((t for t in self.tables if t.get_table_number() == table_number), None)
        if table and (table.is_available() or table.is_reserved()):
            table.occupy_table()
            print(f"Table {table_number} is now occupied")
            return True
        return False

    def release_table(self, table_number: int) -> bool:
        table = next((t for t in self.tables if t.get_table_number() == table_number), None)
        if table and table.is_occupied():
            table.release_table()
            print(f"Table {table_number} is now available")
            return True
        return False

    # Order Processing
    def create_order_with_items(self, table_number: int, customer_name: str, item_orders: List[OrderItem]) -> Optional[Order]:
        """Create an order with multiple items
        item_orders format: [{"item_name": "Pizza", "quantity": 2}, ...]
        """
        with self.processing_lock:
            # Find table and customer
            table = next((t for t in self.tables if t.get_table_number() == table_number), None)

            if not table or not table.is_occupied():
                print(f"Table {table_number} not found or not occupied")
                return None

            # Create order items
            order_items = []
            order_id = str(uuid.uuid4())
            customer = Customer(customer_name)
            for item_order in item_orders:
                item_name = item_order.get_item().get_name()
                quantity = item_order.get_quantity()

                # Find item in menu
                menu_item = next((item for item in self.menu.get_items() if item.get_name().lower() == item_name.lower()), None)
                if not menu_item:
                    raise MissingItemException(f"Item {item_name} not found in menu")
                # Check inventory

                if self.inventory.get_item_quantity(menu_item) < quantity:
                    raise InsufficientStockException(f"Insufficient stock for {item_name}")

                # Create order item
                order_item = OrderItem(order_id, menu_item, quantity)  # order_id will be set when order is created
                order_items.append(order_item)

            # Create order
            order = Order(table_number, order_items, customer)
            self.orders.append(order)

            print(f"Order {order.get_order_id()} created for table {table_number}")
            return order

    def process_order(self, order_id: str) -> bool:
        """Process an order by assigning chef and starting preparation"""
        order = self.get_order_by_id(order_id)
        if not order:
            print(f"Order {order_id} not found")
            return False

        if not self.chefs:
            print("No chefs available")
            return False

        chef = self.chefs[0]  # Assign first available chef

        for order_item in order.get_items():
            # Start preparation
            prepare_command = PrepareOrderCommand(order_item, chef)
            prepare_command.execute()

            # Update inventory
            self.inventory.remove_item(order_item.get_item().get_name(), order_item.get_quantity())

        print(f"Order {order_id} is being prepared by chef {chef.get_name()}")
        return True

    def mark_order_items_ready(self, order_id: str) -> bool:
        """Mark order items as ready for pickup"""
        order = self.get_order_by_id(order_id)

        for order_item in order.get_items():
            order_item.make_ready_for_pickup()
            print(f"Order item {order_item.get_item().get_name()} is ready for pickup")

        return True

    def serve_order(self, order_id: str) -> bool:
        """Serve an order using a waiter"""
        order = self.get_order_by_id(order_id)
        waiter = self.waiters[0]

        if not order or not waiter:
            print(f"Order {order_id} or waiter not found")
            return False

        for order_item in order.get_items():
            serve_command = ServeOrderCommand(order_item, waiter)
            serve_command.execute()

        print(f"Order {order_id} served by waiter {waiter.get_name()}")
        return True

    # Bill Generation
    def generate_bill(self, order_id: str, tax_rate: float = 0.18, service_charge: float = 50.0, discount_percentage: float = 0.0) -> dict:
        """Generate a bill with tax, service charge, and optional discount"""
        order = self.get_order_by_id(order_id)
        if not order:
            return {"error": f"Order {order_id} not found"}

        subtotal = 0.0
        item_details: dict[str, int] = {}
        for order_item in order.get_items():
            # Apply decorators
            decorated_item = ServiceChargeDecorator(
                DiscountDecorator(TaxDecorator(order_item, tax_rate), discount_percentage), service_charge / len(order.get_items())
            )
            subtotal += decorated_item.get_subtotal()
            item_details[order_item.get_item().get_name()] = order_item.get_quantity()

        print(
            f"Bill generated for order {order_id}\n table number: {order.get_table_number()}\n customer: {order.get_ordered_by().get_name()}\n items: {item_details}\n total: ₹{subtotal:.2f}"
        )

    # Payment Processing
    def process_payment(self, payment_method: PaymentStrategy, amount: float) -> Payment:
        return payment_method.pay(amount)
