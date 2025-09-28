from app.observers.base_observer import Subject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionSubject(Subject):
    """Subject for transaction-related notifications"""

    def notify_observers(self, data: "Transaction") -> None:
        for observer in self._observers:
            observer.transaction_update(data)
