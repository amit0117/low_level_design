from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from app.models.enums import ATMStatus, TransactionType
from app.models.card import Card

if TYPE_CHECKING:
    from app.models.atm import ATM


class ATMState(ABC):
    @abstractmethod
    def insert_card(self, atm: "ATM", card: Card) -> None:
        """Insert card action"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def eject_card(self, atm: "ATM") -> None:
        """Eject card action"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def enter_pin(self, atm: "ATM") -> None:
        """Enter PIN action - uses ATM's keypad to read PIN"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def select_transaction(self, atm: "ATM", txn_type: TransactionType) -> None:
        """Select transaction type action"""
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def perform_transaction(self, atm: "ATM", amount: Optional[float] = None) -> None:
        """Perform transaction action"""
        raise NotImplementedError("Subclass must implement this method")
