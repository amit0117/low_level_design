from abc import ABC, abstractmethod
from app.models.payment_response import PaymentResponse
from app.models.enums import PaymentStatus, PaymentMethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResponse:
        raise NotImplementedError("Subclasses must implement this method")


# For now all payment will be successful


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResponse:
        return PaymentResponse(amount, PaymentMethod.CASH, PaymentStatus.PAID)


class CreditCardPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResponse:
        return PaymentResponse(amount, PaymentMethod.CREDIT_CARD, PaymentStatus.PAID)


class DebitCardPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResponse:
        return PaymentResponse(amount, PaymentMethod.DEBIT_CARD, PaymentStatus.PAID)


class UPIPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResponse:
        return PaymentResponse(amount, PaymentMethod.UPI, PaymentStatus.PAID)
