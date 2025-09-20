from app.models.shopping_cart import ShoppingCart
from app.models.order import Order
from app.models.product import Product


class Account:
    def __init__(self, user_id: str, user_name: str, password: str):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.shopping_cart: ShoppingCart = ShoppingCart()
        self.order_history: list[Order] = []

    def get_user_name(self) -> str:
        return self.user_name

    def get_user_id(self) -> str:
        return self.user_id

    def verify_password(self, password: str) -> bool:
        return self.password == password

    def get_cart(self) -> ShoppingCart:
        return self.shopping_cart

    def add_order_to_history(self, order: Order) -> None:
        self.order_history.append(order)

    def remove_order_from_history(self, order_id: str) -> None:
        for order in self.order_history:
            if order.get_order_id() == order_id:
                self.order_history.remove(order)
        print(f"Order with id {order_id} not found in order history")

    def get_order_history(self) -> list[Order]:
        return self.order_history

    def add_to_cart(self, product: Product, quantity: int) -> None:
        self.shopping_cart.add_item(product, quantity)

    def remove_from_cart(self, product: Product, quantity: int) -> None:
        self.shopping_cart.remove_item(product, quantity)
