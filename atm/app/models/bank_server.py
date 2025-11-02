from abc import ABC, abstractmethod
from app.models.card import Card


class BankServer(ABC):
    @abstractmethod
    def validate_card(self, card: Card) -> bool:
        raise NotImplementedError("validate_card method must be implemented")

    @abstractmethod
    def validate_pin(self, card: Card, pin: str) -> bool:
        raise NotImplementedError("validate_pin method must be implemented")

    @abstractmethod
    def get_account_balance(self, account_number: str) -> float:
        raise NotImplementedError("get_account_balance method must be implemented")

    @abstractmethod
    def withdraw(self, account_number: str, amount: float) -> None:
        raise NotImplementedError("withdraw method must be implemented")

    @abstractmethod
    def deposit(self, account_number: str, amount: float) -> None:
        raise NotImplementedError("deposit method must be implemented")

# implement some bank Server like HDFC, SBI, ICICI, also we should use adapter pattern to implement the bank server.