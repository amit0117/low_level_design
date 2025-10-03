from app.models.enums import PaymentMethod, PaymentStatus
from app.models.payment import Payment
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> Payment:
        raise NotImplementedError("Subclasses must implement this method")


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> Payment:
        # Assuming payment is successful
        print(f"Processing credit card payment of {amount}")
        return Payment(amount, PaymentMethod.CREDIT_CARD, PaymentStatus.SUCCESS)


class CashPayment(PaymentStrategy):
    def pay(self, amount: float) -> Payment:
        print(f"Processing cash payment of {amount}")
        return Payment(amount, PaymentMethod.CASH, PaymentStatus.SUCCESS)


class UpiPayment(PaymentStrategy):
    def pay(self, amount: float) -> Payment:
        print(f"Processing upi payment of {amount}")
        return Payment(amount, PaymentMethod.UPI, PaymentStatus.SUCCESS)


class CardPayment(PaymentStrategy):
    def pay(self, amount: float) -> Payment:
        print(f"Processing card payment of {amount}")
        return Payment(amount, PaymentMethod.CARD, PaymentStatus.SUCCESS)
