from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionObserver(ABC):
    @abstractmethod
    def update_on_transaction(self, transaction: "Transaction") -> None:
        raise NotImplementedError("update_on_transaction_status_change method must be implemented")


class TransactionSubject:
    def __init__(self):
        self.observers: list[TransactionObserver] = []

    def add_observer(self, observer: TransactionObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: TransactionObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, transaction: "Transaction") -> None:
        print(f"Notifying {len(self.observers)} observers about transaction {transaction.get_transaction_id()}")
        for observer in self.observers:
            observer.update_on_transaction(transaction)
