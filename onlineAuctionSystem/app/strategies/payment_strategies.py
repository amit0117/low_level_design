from app.models.payment_response import PaymentResponse
from app.models.enums import PaymentStatus, PaymentMethod
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResponse:
        raise NotImplementedError("Pay method has not been implemented")


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, expiry_date: str, cvv: str):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv

    def pay(self, amount: float) -> PaymentResponse:
        print(f"Processing credit card payment of {amount} with card number {self.card_number}")
        return PaymentResponse(PaymentStatus.SUCCESS, PaymentMethod.CREDIT_CARD)


class DebitCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, expiry_date: str, cvv: str):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cvv = cvv

    def pay(self, amount: float) -> PaymentResponse:
        print(f"Processing debit card payment of {amount} with card number {self.card_number}")
        return PaymentResponse(PaymentStatus.SUCCESS, PaymentMethod.DEBIT_CARD)


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResponse:
        print(f"Processing cash payment of {amount}")
        return PaymentResponse(PaymentStatus.SUCCESS, PaymentMethod.CASH)
