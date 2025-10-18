from app.strategies.payment_strategies import PaymentStrategy
from app.models.payment_response import PaymentResponse
from typing import Optional


class PaymentService:
    def __init__(self, payment_strategy: Optional[PaymentStrategy] = None):
        self.payment_strategy = payment_strategy

    def process_payment(self, amount: float) -> PaymentResponse:
        if not self.payment_strategy:
            raise ValueError("Payment strategy is not set")
        return self.payment_strategy.pay(amount)

    def refund_payment(self, amount: float) -> PaymentResponse:
        raise NotImplementedError("Refund payment is not implemented Yet")
