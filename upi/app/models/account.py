from app.models.enums import AccountType, PaymentType
from app.models.transaction import Transaction
from app.observers.account_observer import AccountSubject
from typing import TYPE_CHECKING
from threading import Lock
from app.exceptions.insufficient_fund import InsufficientFundsException

if TYPE_CHECKING:
    from app.models.user import User


class Account(AccountSubject):
    def __init__(self, account_number: str, account_type: AccountType, balance: float, user: "User", bank_name: str):
        super().__init__()
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.user = user
        self.bank_name = bank_name
        self.transactions: list[Transaction] = []
        self.lock = Lock()

    def get_account_number(self) -> str:
        return self.account_number

    def get_account_type(self) -> AccountType:
        return self.account_type

    def get_balance(self) -> float:
        return self.balance

    def get_user(self) -> "User":
        return self.user

    def get_vpa(self) -> str:
        return f"{self.user.get_name()}@{self.get_bank_name()}"

    def get_bank_name(self) -> str:
        return self.bank_name

    def add_transaction(self, transaction: Transaction) -> None:
        with self.lock:
            self.transactions.append(transaction)

    def get_transaction_history(self) -> list[Transaction]:
        return self.transactions

    def withdraw(self, amount: float) -> None:
        with self.lock:
            if self.balance < amount:
                raise InsufficientFundsException()
            self.balance -= amount
            self.notify_observers(self, amount, PaymentType.DEBIT)

    def deposit(self, amount: float) -> None:
        with self.lock:
            self.balance += amount
            self.notify_observers(self, amount, PaymentType.CREDIT)

    def get_balance(self) -> float:
        return self.balance
