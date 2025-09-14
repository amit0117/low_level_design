from threading import Lock
from typing import Optional
from app.models.user import User
from app.models.stock import Stock


class StockBrokerageSystem:
    _lock = Lock()
    _instance: Optional["StockBrokerageSystem"] = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._has_initialized:
            self._users: dict[str, User] = {}
            self._stocks: dict[str, Stock] = {}
            self.process_lock = Lock()
            self._has_initialized = True
        return

    @classmethod
    def get_instance(cls):
        cls()

    def register_user(self, user: User):
        with self.process_lock:
            if user.user_id in self._users:
                raise Exception(f"User {user.user_id} already exists")
            self._users[user.user_id] = user

    def remove_user(self, user: User):
        with self.process_lock:
            if user.user_id not in self._users:
                raise Exception(f"User {user.user_id} does not exist")
            del self._users[user.user_id]

    def add_stock(self, stock: Stock):
        with self.process_lock:
            self._stocks[stock.get_symbol()] = stock

    def remove_stock(self, stock: Stock):
        with self.process_lock:
            if stock.get_symbol() not in self._stocks:
                raise Exception(f"Stock {stock.get_symbol()} does not exist")
            del self._stocks[stock.get_symbol()]

    def place_buy_order
