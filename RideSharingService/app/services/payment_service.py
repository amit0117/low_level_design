from app.strategies.payment_strategy import PaymentStrategy
from app.models.payment_result import PaymentResult


class PaymentService:
    def __init__(self) -> None:
        self.payments: dict[str, PaymentResult] = {}
        self.payment_strategy: PaymentStrategy = None

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self.payment_strategy = strategy

    def process_payment(self, amount: float) -> PaymentResult:
        return self.payment_strategy.pay(amount)

    def get_payment(self, transaction_id: str) -> PaymentResult:
        if transaction_id not in self.payments:
            print(f"Payment with transaction id {transaction_id} not found")
            return None
        return self.payments[transaction_id]

    def get_all_payments(self) -> list[PaymentResult]:
        return list(self.payments.values())
