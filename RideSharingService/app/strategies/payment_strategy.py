from abc import ABC, abstractmethod
from app.models.payment_result import PaymentResult
from app.models.enums import PaymentStatus, PaymentMethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        raise NotImplementedError("Subclasses must implement this method")


# For simplicity returning success payment for all payment strategies
class CreditCardPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Processing credit card payment of ${amount}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CREDIT_CARD)


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Processing cash payment of ${amount}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CASH)


class DebitCardPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Processing debit card payment of ${amount}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.DEBIT_CARD)


class UPIPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Processing UPI payment of ${amount}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.UPI)
