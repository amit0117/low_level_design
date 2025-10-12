from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import PaymentMethod, PaymentStatus, TransactionStatus

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionState(ABC):
    @abstractmethod
    def cancel(self, transaction: "Transaction") -> bool:
        raise NotImplementedError("cancel method must be implemented")

    @abstractmethod
    def refund(self, transaction: "Transaction") -> bool:
        raise NotImplementedError("refund method must be implemented")

    @abstractmethod
    def process(self, transaction: "Transaction") -> bool:
        raise NotImplementedError("process method must be implemented")


class PendingState(TransactionState):
    def cancel(self, transaction: "Transaction") -> bool:
        # Check For Pull , Push and other payment methods
        transaction_payment_status = transaction.get_payment().get_status()
        # Irrespective of the payment method, we can only cancel the transaction if the payment is pending
        transaction.set_state(CancelledState())
        transaction.set_status(TransactionStatus.CANCELLED)
        return True

    def refund(self, transaction: "Transaction") -> bool:
        print("Cannot refund a pending transaction")
        return False

    def process(self, transaction: "Transaction") -> bool:
        # For pull payment method, we can only process the transaction if the payment is Approved
        payment_method = transaction.get_payment().get_payment_method()
        transaction_payment_status = transaction.get_payment().get_status()
        if payment_method != PaymentMethod.UPI_PULL:
            # We can always process the transaction for push payment method
            transaction.set_state(SuccessState())
            transaction.set_status(TransactionStatus.SUCCESS)
            return True
        elif transaction_payment_status == PaymentStatus.APPROVED:
            # For pull payment method, we can only process the transaction if the payment is Approved
            transaction.set_state(SuccessState())
            transaction.set_status(TransactionStatus.SUCCESS)
            return True
        return False


class SuccessState(TransactionState):
    def cancel(self, transaction: "Transaction") -> bool:
        print("Cannot cancel a successful transaction")
        return False

    def refund(self, transaction: "Transaction") -> bool:
        transaction.set_state(RefundedState())
        transaction.set_status(TransactionStatus.REFUNDED)
        return True

    def process(self, transaction: "Transaction") -> bool:
        print("Cannot process a successful transaction")
        return False


class FailedState(TransactionState):
    def cancel(self, transaction: "Transaction") -> bool:
        transaction.set_state(CancelledState())
        transaction.set_status(TransactionStatus.CANCELLED)
        return True

    def refund(self, transaction: "Transaction") -> bool:
        transaction.set_state(RefundedState())
        transaction.set_status(TransactionStatus.REFUNDED)
        return True

    def process(self, transaction: "Transaction") -> bool:
        print("Cannot process a failed transaction")
        return False


class RefundedState(TransactionState):
    def cancel(self, transaction: "Transaction") -> bool:
        print("Cannot cancel a refunded transaction")
        return False

    def refund(self, transaction: "Transaction") -> bool:
        print("Cannot refund a refunded transaction")
        return False

    def process(self, transaction: "Transaction") -> bool:
        print("Cannot process a refunded transaction")
        return False


class CancelledState(TransactionState):
    def cancel(self, transaction: "Transaction") -> bool:
        print("Cannot cancel a cancelled transaction")
        return False

    def refund(self, transaction: "Transaction") -> bool:
        print("Cannot refund a cancelled transaction")
        return False

    def process(self, transaction: "Transaction") -> bool:
        print("Cannot process a cancelled transaction")
        return False
