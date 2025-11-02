# Template method pattern
# In your ATM, each transaction (Withdraw, Deposit, Transfer) follows a common skeleton:
# validate() → authorize() → performTransaction() → dispenseOrAccept() → printReceipt()

from abc import ABC, abstractmethod
from app.observers.subjects import BaseSubject


class Transaction(ABC, BaseSubject):
    def __init__(self):
        BaseSubject.__init__(self)

    # This method should not be overridden by the subclasses
    def execute(self) -> None:
        self.validate()
        self.authorize()
        try:
            self.perform_transaction()
            self.dispense_or_accept()
            self.print_receipt()
            # Notify observers on successful completion
            self.notify_observers(self._get_success_message())
        except Exception as e:
            print(f"Transaction failed: {e}")
            self.rollback()
            # Notify observers on failure
            self.notify_observers(f"Transaction failed: {e}")

    def _get_success_message(self) -> str:
        return "Transaction completed successfully"

    @abstractmethod
    def validate(self) -> None:
        raise NotImplementedError("validate method must be implemented")

    @abstractmethod
    def authorize(self) -> None:
        raise NotImplementedError("authorize method must be implemented")

    @abstractmethod
    def perform_transaction(self) -> None:
        raise NotImplementedError("perform_transaction method must be implemented")

    @abstractmethod
    def dispense_or_accept(self) -> None:
        raise NotImplementedError("dispense_or_accept method must be implemented")

    @abstractmethod
    def print_receipt(self) -> None:
        raise NotImplementedError("print_receipt method must be implemented")

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError("rollback method must be implemented")
