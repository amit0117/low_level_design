from abc import ABC, abstractmethod
from app.models.enums import PaymentStatus
import time


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentStatus:
        raise NotImplementedError("subclass must implement this method")


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> PaymentStatus:
        print(f"Processing credit card payment of {amount} with card {self.card_number}")
        # Simulating the payment processing time
        time.sleep(1)
        return PaymentStatus.COMPLETED


class DebitCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> PaymentStatus:
        print(f"Processing debit card payment of {amount} with card {self.card_number}")
        # Simulating the payment processing time
        time.sleep(1)
        return PaymentStatus.COMPLETED


class UpiPaymentStrategy(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> PaymentStatus:
        print(f"Processing upi payment of {amount} with id {self.upi_id}")
        # Simulating the payment processing time
        time.sleep(1)
        return PaymentStatus.COMPLETED


class CashOnDeliveryPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentStatus:
        print(f"Processing cash on delivery payment of {amount}")
        # Simulating the payment processing time
        time.sleep(1)
        return PaymentStatus.COMPLETED
