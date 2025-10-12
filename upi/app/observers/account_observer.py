from abc import ABC, abstractmethod
from app.models.enums import PaymentType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.account import Account


class AccountObserver(ABC):
    @abstractmethod
    def update_on_account_balance_change(self, account: "Account", amount: float, payment_type: PaymentType) -> None:
        raise NotImplementedError("update_on_account_balance_change method must be implemented")


class AccountSubject:
    def __init__(self):
        self.observers: list[AccountObserver] = []

    def add_observer(self, observer: AccountObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: AccountObserver) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, account: "Account", amount: float, payment_type: PaymentType) -> None:
        print(f"Notifying {len(self.observers)} observers about account balance change")
        for observer in self.observers:
            observer.update_on_account_balance_change(account, amount, payment_type)
