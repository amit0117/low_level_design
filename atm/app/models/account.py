from threading import Lock
from app.exceptions.insufficient_money import InsufficientFundsException
from typing import TYPE_CHECKING
from app.models.enums import AccountType

if TYPE_CHECKING:
    from app.models.user import User


class Account:
    def __init__(self, account_number: str, account_type: AccountType, balance: float, user: "User", bank_name: str):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.user = user
        self.bank_name = bank_name
        self.lock = Lock()

    def get_account_number(self) -> str:
        return self.account_number

    def get_account_type(self) -> AccountType:
        return self.account_type

    def get_balance(self) -> float:
        with self.lock:
            return self.balance

    def get_user(self) -> "User":
        return self.user

    def get_bank_name(self) -> str:
        return self.bank_name

    def withdraw(self, amount: float) -> None:
        with self.lock:
            if self.balance < amount:
                raise InsufficientFundsException()
            self.balance -= amount

    def deposit(self, amount: float) -> None:
        with self.lock:
            self.balance += amount
