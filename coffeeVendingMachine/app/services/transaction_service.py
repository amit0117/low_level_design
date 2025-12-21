from app.models.enums import Coin
from app.services.payment_processor import PaymentProcessor


class TransactionService:
    def __init__(self):
        self.payment_processor = PaymentProcessor()

    def validate_payment(self, price: float, coins: list[Coin]) -> tuple[bool, float]:
        is_valid, paid_amount = self.payment_processor.process_payment(price, coins)
        return is_valid, paid_amount

    def calculate_change(self, paid: float, price: float) -> float:
        return self.payment_processor.calculate_change(paid, price)
