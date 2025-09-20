from typing import Optional
from app.models.order import Order
from app.models.enums import PaymentStatus, PaymentMethod
from app.models.payment_strategy import PaymentStrategy
from uuid import uuid4
import time


class PaymentResult:
    def __init__(self, success: bool, transaction_id: str = None, error_message: str = None):
        self.success = success
        self.transaction_id = transaction_id
        self.error_message = error_message


class PaymentService:
    """Service for processing payments"""

    def __init__(self):
        self.transactions: dict[str, dict] = {}

    def process_payment(self, payment_strategy: PaymentStrategy, amount: float) -> PaymentResult:
        """Process payment for an order"""

        # Simulate payment processing
        transaction_id = f"TXN_{uuid4()}"
        payment_status = payment_strategy.pay(amount)

        if payment_status == PaymentStatus.COMPLETED:
            self.transactions[transaction_id] = {
                "amount": amount,
                "status": payment_status,
            }
            return PaymentResult(True, transaction_id)
        else:
            return PaymentResult(False, error_message=f"Payment processing failed with status {payment_status}")

    def refund_payment(self, transaction_id: str, amount: float = None) -> PaymentResult:
        """Process refund for a transaction"""
        if transaction_id not in self.transactions:
            return PaymentResult(False, error_message="Transaction not found")

        transaction = self.transactions[transaction_id]
        refund_amount = amount or transaction["amount"]

        # Simulate refund processing
        refund_success = self._simulate_refund_processing(transaction_id, refund_amount)

        if refund_success:
            transaction["status"] = PaymentStatus.REFUNDED
            return PaymentResult(True, f"REFUND_{transaction_id}")
        else:
            return PaymentResult(False, error_message="Refund processing failed")

    def get_transaction(self, transaction_id: str) -> Optional[dict]:
        """Get transaction details"""
        return self.transactions.get(transaction_id)

    def _simulate_refund_processing(self, transaction_id: str, amount: float) -> bool:
        """Simulate refund processing"""
        # In a real system, this would call payment gateway refund API
        time.sleep(1)
        return True
