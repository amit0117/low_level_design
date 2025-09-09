from app.models.account import Account
from app.models.stock import Stock
from app.models.stock_observer import StockObserver
from app.models.order import Order
from uuid import uuid4


class User(StockObserver):
    def __init__(self, name: str):
        self.user_id = str(uuid4())
        self.name = name
        self.account = Account()
        self.orders: list[Order] = []

    def get_name(self) -> str:
        return self.name

    def get_account(self) -> Account:
        return self.account

    def get_orders(self) -> list[Order]:
        return self.orders.copy()

    def update(self, stock: Stock):
        print(
            f"User {self.name} notified about stock {stock.symbol} price change to {stock.get_price():.2f}"
        )

    def order_status_update(self, order: Order):
        print(
            f"User {self.name} notified about order {order.order_id} status change to {order.get_status().value} for stock {order.get_stock().get_symbol()} at price {order.get_price():.2f} and quantity {order.get_quantity()}"
        )
