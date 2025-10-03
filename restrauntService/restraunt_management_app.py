import threading
from typing import List, Optional
from app.services.table_service import TableService
from app.services.order_service import OrderService
from app.services.inventory_service import InventoryService
from app.services.staff_service import StaffService
from app.services.menu_service import MenuService
from app.models.staff import Manager, Chef, Waiter
from app.models.table import Table
from app.models.item import Item
from app.models.order import Order
from app.models.order_item import OrderItem
from app.decorators.bill_decorator import TaxDecorator, ServiceChargeDecorator, DiscountDecorator
from app.strategies.payment_strategy import PaymentStrategy, Payment


class RestrauntManagementApp:
    """
    Facade class that provides a simplified interface to the restaurant management system.
    This class coordinates between repositories and services to provide high-level operations.
    """

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
            # Initialize services - repositories are now singletons
            # Each service will get the same repository instance automatically
            self.table_service = TableService()
            self.order_service = OrderService()
            self.inventory_service = InventoryService()
            self.staff_service = StaffService()
            self.menu_service = MenuService()

            self.processing_lock = threading.Lock()
            self._initialized = True

    @classmethod
    def get_instance(cls) -> "RestrauntManagementApp":
        return cls()

    # ==================== FACADE METHODS - SIMPLIFIED INTERFACE ====================

    # Table Management Facade Methods
    def add_table(self, table: Table) -> None:
        """Add table to the system"""
        self.table_service.add_table(table)

    def reserve_table(self, table_number: int, customer_name: str, size: int) -> bool:
        """Reserve a table for a customer"""
        return self.table_service.reserve_table(table_number, customer_name, size)

    def occupy_table(self, table_number: int) -> bool:
        """Occupy a table"""
        return self.table_service.occupy_table(table_number)

    def release_table(self, table_number: int) -> bool:
        """Release a table"""
        return self.table_service.release_table(table_number)

    def get_available_tables(self) -> List[Table]:
        """Get all available tables"""
        return self.table_service.get_available_tables()

    def get_tables(self) -> List[Table]:
        """Get all tables"""
        return self.table_service.get_all_tables()

    # Staff Management Facade Methods
    def add_manager(self, manager: Manager) -> None:
        """Add manager to the system"""
        self.staff_service.add_staff_member(manager)

    def add_chef(self, chef: Chef) -> None:
        """Add chef to the system"""
        self.staff_service.add_staff_member(chef)

    def add_waiter(self, waiter: Waiter) -> None:
        """Add waiter to the system"""
        self.staff_service.add_staff_member(waiter)

    def get_chefs(self) -> List[Chef]:
        """Get all chefs"""
        return self.staff_service.get_all_chefs()

    def get_waiters(self) -> List[Waiter]:
        """Get all waiters"""
        return self.staff_service.get_all_waiters()

    def get_managers(self) -> List[Manager]:
        """Get all managers"""
        return self.staff_service.get_all_managers()

    # Menu Management Facade Methods
    def get_menu(self) -> MenuService:
        """Get menu service"""
        return self.menu_service

    def add_item_to_menu(self, item: Item) -> None:
        """Add item to menu"""
        self.menu_service.add_item_to_menu(item)

    def remove_item_from_menu(self, item: Item) -> None:
        """Remove item from menu"""
        self.menu_service.remove_item_from_menu(item)

    # Inventory Management Facade Methods
    def get_inventory(self) -> InventoryService:
        """Get inventory service"""
        return self.inventory_service

    def add_item_to_inventory(self, item: Item, quantity: int) -> None:
        """Add item to inventory"""
        self.inventory_service.add_item_to_inventory(item, quantity)

    def remove_item_from_inventory(self, item: Item, quantity: int) -> None:
        """Remove item from inventory"""
        self.inventory_service.remove_item_from_inventory(item, quantity)

    # Order Management Facade Methods
    def create_order(self, table: Table, order_items: List[OrderItem], ordered_by: str) -> Order:
        """Create order (legacy method for compatibility)"""
        with self.processing_lock:
            # Use OrderService to create order
            return self.order_service.create_order(table.get_table_number(), ordered_by, order_items)

    def create_order_with_items(self, table_number: int, customer_name: str, item_orders: List[OrderItem]) -> Optional[Order]:
        """Create order with items - delegates to OrderService"""
        return self.order_service.create_order(table_number, customer_name, item_orders)

    def get_orders(self) -> List[Order]:
        """Get all orders"""
        return self.order_service.get_all_orders()

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.order_service.get_order_by_id(order_id)

    def process_order(self, order_id: str) -> bool:
        """Process order - delegates to OrderService"""
        chef = self.staff_service.get_available_chef()
        if not chef:
            print("No chefs available")
            return False
        return self.order_service.process_order(order_id, chef)

    def mark_order_items_ready(self, order_id: str) -> bool:
        """Mark order items ready - delegates to OrderService"""
        return self.order_service.mark_order_items_ready(order_id)

    def serve_order(self, order_id: str) -> bool:
        """Serve order - delegates to OrderService"""
        waiter = self.staff_service.get_available_waiter()
        if not waiter:
            print("No waiters available")
            return False
        return self.order_service.serve_order(order_id, waiter)

    # Bill Generation Facade Methods
    def generate_bill(self, order_id: str, tax_rate: float = 0.18, service_charge: float = 50.0, discount_percentage: float = 0.0) -> dict:
        """Generate bill with tax, service charge, and optional discount"""
        order = self.order_service.get_order_by_id(order_id)
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
            f"Bill generated for order {order_id}\n"
            f"table number: {order.get_table_number()}\n"
            f"customer: {order.get_ordered_by().get_name()}\n"
            f"items: {item_details}\n"
            f"total: ₹{subtotal:.2f}"
        )

    # Payment Processing Facade Methods
    def process_payment(self, payment_method: PaymentStrategy, amount: float) -> Payment:
        """Process payment - delegates to payment strategy"""
        return payment_method.pay(amount)

    # ==================== COMPLEX WORKFLOW METHODS ====================

    def complete_dining_experience(
        self, table_number: int, customer_name: str, item_orders: List[OrderItem], chef_name: str = None, waiter_name: str = None
    ) -> Optional[Order]:
        """
        Complete dining experience workflow - a complex operation that orchestrates multiple services
        This is a perfect example of Facade pattern simplifying complex operations
        """
        try:
            # Step 1: Reserve table
            if not self.reserve_table(table_number, customer_name, len(item_orders)):
                return None

            # Step 2: Occupy table
            if not self.occupy_table(table_number):
                return None

            # Step 3: Create order
            order = self.create_order_with_items(table_number, customer_name, item_orders)
            if not order:
                return None

            # Step 4: Process order
            if chef_name:
                chef = self.staff_service.get_all_chefs()
                chef = next((c for c in chef if c.get_name() == chef_name), None)
                if chef:
                    self.order_service.process_order(order.get_order_id(), chef)
            else:
                self.process_order(order.get_order_id())

            # Step 5: Mark ready
            self.mark_order_items_ready(order.get_order_id())

            # Step 6: Serve order
            if waiter_name:
                waiters = self.staff_service.get_all_waiters()
                waiter = next((w for w in waiters if w.get_name() == waiter_name), None)
                if waiter:
                    self.order_service.serve_order(order.get_order_id(), waiter)
            else:
                self.serve_order(order.get_order_id())

            return order

        except Exception as e:
            print(f"Error in complete dining experience: {e}")
            return None

    def get_restaurant_status(self) -> dict:
        """Get comprehensive restaurant status - orchestrates multiple services"""
        table_status = self.table_service.get_table_status()
        order_status = self.order_service.get_order_status()
        staff_status = self.staff_service.get_staff_status()
        inventory_status = self.inventory_service.get_inventory_status()

        return {
            "tables": table_status,
            "orders": order_status,
            "staff": staff_status,
            "inventory": inventory_status,
            "menu_items": len(self.menu_service.get_all_items()),
        }

    def print_restaurant_status(self) -> None:
        """Print formatted restaurant status"""
        status = self.get_restaurant_status()
        print("\n" + "=" * 40)
        print("RESTAURANT STATUS")
        print("=" * 40)
        print(f"Tables: {status['tables']['available']}/{status['tables']['total']} available")
        print(f"Staff: {status['staff']['chefs']} chefs, {status['staff']['waiters']} waiters")
        print(f"Orders: {status['orders']['active']}/{status['orders']['total']} active")
        print(f"Menu Items: {status['menu_items']}")
        print(f"Inventory: {status['inventory']['available_items']} items available")
        print("=" * 40)
