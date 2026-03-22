from __future__ import annotations
from app.utils import SingletonMeta
from threading import Lock
from app.models.user import User
from app.models.stock import Stock
from app.models.order import Order
from app.models.order_command import BuyStockCommand, SellStockCommand, CancelOrderCommand


class StockBrokerageSystem(metaclass=SingletonMeta):

    def __init__(self):
        self._users: dict[str, User] = {}
        self._stocks: dict[str, Stock] = {}
        self.process_lock = Lock()

    def register_user(self, user: User) -> None:
        with self.process_lock:
            if user.user_id in self._users:
                print(f"User {user.user_id} already exists")
                return
            self._users[user.user_id] = user

    def remove_user(self, user: User) -> None:
        with self.process_lock:
            if user.user_id not in self._users:
                print(f"User {user.user_id} does not exist")
                return
            del self._users[user.user_id]

    def get_all_stocks(self) -> dict[str, Stock]:
        return self._stocks

    def get_all_users(self) -> dict[str, User]:
        # Return users by name instead of ID for easier access in demo
        return {user.get_name(): user for user in self._users.values()}

    def add_stock(self, stock: Stock) -> None:
        with self.process_lock:
            if stock.get_symbol() in self._stocks:
                print(f"Stock {stock.get_symbol()} already exists")
                return
            self._stocks[stock.get_symbol()] = stock

    def remove_stock(self, stock: Stock) -> None:
        with self.process_lock:
            if stock.get_symbol() not in self._stocks:
                print(f"Stock {stock.get_symbol()} does not exist")
                return
            del self._stocks[stock.get_symbol()]

    def place_buy_order(self, order: Order) -> None:
        user = order.get_owner()
        command = BuyStockCommand(user.get_account(), order)
        command.execute()

    def place_sell_order(self, order: Order) -> None:
        user = order.get_owner()
        command = SellStockCommand(user.get_account(), order)
        command.execute()

    def cancel_order(self, order: Order) -> None:
        command = CancelOrderCommand(order)
        command.execute()
