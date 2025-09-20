from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.search_service import SearchService
from app.services.inventory_service import InventoryService
from threading import Lock
from app.models.user import User
from app.models.product import Product
from app.models.payment_strategy import PaymentStrategy
from app.models.enums import OrderStatus
from app.models.order_states import PlacedState, PendingState, CancelledState
from app.models.order import Order
from app.models.exceptions import InsufficientStockException, InsufficientFundsException, OutOfStockException
from app.models.search_strategy import SearchStrategy
from typing import Any, Optional


# Will act as a facade for the online shopping service system
class OnlineShoppingServiceSystem:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._has_initialized = False
        return cls._instance

    def __init__(self):
        if self._has_initialized:
            return
        self.user_service = UserService()
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.search_service = SearchService()
        self.inventory_service = InventoryService()
        self._has_initialized = True

    @classmethod
    def get_instance(cls) -> "OnlineShoppingServiceSystem":
        return cls()

    def register_user(self, user: User) -> None:
        self.user_service.add_user(user)

    def login_user(self, user_name: str, password: str) -> None:
        is_authenticated = self.user_service.authenticate_user(user_name, password)
        if is_authenticated:
            print(f"User {user_name} logged in successfully")
        print(f"User {user_name} failed to log in")

    def add_product(self, product: Product) -> None:
        self.inventory_service.add_product(product)

    def add_product_to_cart(self, user: User, product: Product, quantity: int) -> None:
        user.get_account().get_cart().add_item(product, quantity)

    def remove_product_from_cart(self, user: User, product: Product) -> None:
        user.get_account().get_cart().remove_item(product)

    def update_product_in_cart(self, user: User, product: Product, quantity: int) -> None:
        user.get_account().get_cart().add_item(product, quantity)

    def remove_product(self, product: Product) -> None:
        self.inventory_service.remove_product(product)

    def search_products(self, search_strategy: SearchStrategy, keyword: Any) -> list[Product]:
        self.search_service.set_strategy(search_strategy)
        print(f"Searching for {keyword} with strategy {search_strategy}")
        return self.search_service.search(keyword)

    def place_order(self, user: User, payment_strategy: PaymentStrategy) -> Optional[Order]:
        cartItems = user.get_account().get_cart().get_items()

        if not cartItems:
            print("Cannot place an order with an empty cart.")
            return None
        order = self.order_service.create_order_from_cart(user, cartItems)
        # Before placing the order, set the order status to pending and state to pending
        order.set_status(OrderStatus.PENDING)
        order.set_state(PendingState())

        if not self._validate_inventory(order):
            print("Inventory stocks are not valid.Cannot place the order. Please try again.")
            return None
        # Assuming user has enough funds
        total_price = order.get_total_price()
        payment_result = self.payment_service.process_payment(payment_strategy, total_price)

        if payment_result.success:
            print("Payment successful. Placing the order.")
            # update the order status and state
            order.set_status(OrderStatus.PLACED)
            order.set_state(PlacedState())
            self._update_inventory(order)
            # clear the cart
            user.get_account().get_cart().clear()
            # add the order to the order history
            user.get_account().add_order_to_history(order)
            return order
        else:
            order.set_status(OrderStatus.CANCELLED)
            order.set_state(CancelledState())
            print("Payment failed. Please try again.")
            return None

    def _validate_inventory(self, order: Order) -> bool:
        for item in order.get_order_items():
            if not self.inventory_service.is_product_available(item.get_product_id()):
                print(f"Product {item.get_product_id()} is not available")
                raise OutOfStockException(f"Product {item.get_product_id()} is not available")
            if self.inventory_service.get_product_stock_count(item.get_product_id()) < item.get_quantity():
                print(
                    f"Product {item.get_product_id()} has insufficient stock, found {self.inventory_service.get_product_stock_count(item.get_product_id())} but required {item.get_quantity()}"
                )
                raise InsufficientStockException(f"Product {item.get_product_id()} has insufficient stock")
        return True

    def _update_inventory(self, order: Order) -> None:
        for item in order.get_order_items():
            self.inventory_service.update_stock(item.get_product_id(), -1 * item.get_quantity())
