from app.strategies.payment_strategy import PaymentStrategy
from app.models.payment_result import PaymentResult


class PaymentService:
    def __init__(self) -> None:
        self.payment_strategy: PaymentStrategy = None

    def set_payment_strategy(self, payment_strategy: PaymentStrategy) -> None:
        self.payment_strategy = payment_strategy

    def process_payment(self, amount: float) -> PaymentResult:
        if self.payment_strategy is None:
            raise ValueError("Payment strategy is not set")
        return self.payment_strategy.pay(amount)
