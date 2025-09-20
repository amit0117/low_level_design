from app.models.address import Address
from app.models.enums import UserType, OrderStatus
from app.models.account import Account
from app.models.observers.order_observer import OrderObserver
from app.models.observers.inventory_observer import InventoryObserver
from app.models.product import Product
from app.models.order import Order
from uuid import uuid4


# A general user might be a normal user so we it should be able to subscribe in stock to out of stock observer as well as order observer
class User(InventoryObserver, OrderObserver):
    def __init__(self, user_name: str, password: str, shipping_address: Address, user_type: UserType = UserType.NORMAL_USER) -> None:
        super().__init__()
        self.user_id = str(uuid4())
        self.user_name = user_name
        self.shipping_address = shipping_address
        self.user_type = user_type
        self.account: Account = Account(self.user_id, user_name, password)

    def get_user_id(self) -> str:
        return self.user_id

    def get_user_name(self) -> str:
        return self.user_name

    def get_shipping_address(self) -> Address:
        return self.shipping_address

    def get_user_type(self) -> UserType:
        return self.user_type

    def get_account(self) -> Account:
        return self.account

    def set_address(self, shipping_address: Address) -> None:
        self.shipping_address = shipping_address

    def set_user_type(self, user_type: UserType) -> None:
        self.user_type = user_type

    def set_user_name(self, user_name: str) -> None:
        self.user_name = user_name

    def update_about_stock(self, user_type: UserType, product: Product) -> None:
        # Update out of stock to only admins
        if not product.is_available() and user_type != UserType.ADMIN:
            return
        print(f"{user_type.value} {self.user_name} received update about stock of {product.get_name()} which is now {product.get_status().value}")

    def update_about_order(self, order: Order) -> None:
        if order.get_status() == OrderStatus.PLACED:
            print(f"Your order {order.get_order_id()} has been placed")
            return
        # use generic message for other statuses
        print(f"Status of order {order.get_order_id()} is updated to {order.get_status()}")
