from threading import Lock
from app.observers.subjects import BaseSubject
from app.models.user import Admin
from app.exceptions.insufficient_money import InsufficientCashException
from uuid import uuid4


class CashDispenser(BaseSubject):
    def __init__(self, initial_cash: float, low_cash_threshold: float = 1000):
        BaseSubject.__init__(self)
        self.id = str(uuid4())
        self.cash_available = initial_cash
        self.lock = Lock()
        self.low_cash_threshold = low_cash_threshold

    def dispense_cash(self, amount: int) -> None:
        with self.lock:
            if amount > self.cash_available:
                raise ValueError("Insufficient cash available in the ATM.")
            self.cash_available -= amount
            print(f"Cash dispensed: {amount}")

    def add_admin_observer(self, admin: Admin) -> None:
        self.add_observer(admin)

    def remove_admin_observer(self, admin: Admin) -> None:
        self.remove_observer(admin)

    def notify_about_low_cash(self) -> None:
        with self.lock:
            if self.cash_available < self.low_cash_threshold:
                message = f"Low cash available in the ATM threshold was {self.low_cash_threshold}. Current cash available: {self.cash_available}. Please add cash."
                self.notify_observers(message)

    def add_cash(self, amount: float, admin: Admin) -> None:
        with self.lock:
            self.cash_available += amount
            print(f"Cash added: {amount}")
            # Notify the observers about the added cash
            self.notify_observers(
                f"Amount {amount} added by admin {admin.get_name()} to the ATM {self.id[:8]:10s}. \nCurrent cash available: {self.cash_available:.2f}\n\n"
            )

    def remove_cash(self, amount: float) -> None:
        with self.lock:
            if amount > self.cash_available:
                raise InsufficientCashException()
            self.cash_available -= amount
            # Notify the observers about the removed cash
            self.notify_observers(f"Amount {amount} removed from the ATM {self.id[:8]:10s}. \nCurrent cash available: {self.cash_available:.2f}\n\n")
            self.notify_about_low_cash()

    def has_sufficient_cash(self, amount: int) -> bool:
        with self.lock:
            return self.cash_available >= amount

    def get_cash_available(self) -> float:
        with self.lock:
            return self.cash_available
