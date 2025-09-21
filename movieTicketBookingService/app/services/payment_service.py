from app.models.strategy.payment_strategy import PaymentStrategy
from app.models.payment import PaymentResult


class PaymentService:
    def __init__(self) -> None:
        self.payment_history: dict[str, list[PaymentResult]] = {}  # Append only on creation of payment

    def process_payment(self, amount: float, payment_strategy: PaymentStrategy) -> PaymentResult:
        payment_result = payment_strategy.pay(amount)
        return payment_result
