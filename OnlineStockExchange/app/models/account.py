from app.exceptions import InsufficientFundException, InsufficientStockException
from threading import Lock
from uuid import uuid4


class Account:
    def __init__(self, initial_balance: float = 0):
        self.account_id = str(uuid4())
        self.balance = initial_balance
        self.portfolio: dict[str, int] = {}
        self._lock = Lock()

    def debit(self, amount: float):
        with self._lock:
            if amount > self.balance:
                raise InsufficientFundException(f"Insufficient fund to debit {amount}")
            self.balance -= amount

    def credit(self, amount: float):
        with self._lock:
            self.balance += amount

    def add_stock(self, stock_symbol: str, quantity: int):
        with self._lock:
            self.portfolio[stock_symbol] = (
                self.portfolio.get(stock_symbol, 0) + quantity
            )

    def remove_stock(self, stock_symbol: str, quantity: int):
        with self._lock:
            if (
                stock_symbol not in self.portfolio
                or self.portfolio[stock_symbol] < quantity
            ):
                raise InsufficientStockException(
                    f"Insufficient stock {stock_symbol} to remove {quantity}"
                )

            self.portfolio[stock_symbol] -= quantity
            if self.portfolio[stock_symbol] == 0:
                del self.portfolio[stock_symbol]

    def get_balance(self) -> float:
        return self.balance

    def get_portfolio(self) -> dict[str, int]:
        return self.portfolio.copy()

    def get_stock_quantity(self, stock_symbol: str) -> int:
        return self.portfolio.get(stock_symbol, 0)
