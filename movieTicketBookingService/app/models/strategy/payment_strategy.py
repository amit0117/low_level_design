from abc import ABC, abstractmethod
from app.models.payment import PaymentResult
from app.models.enums import PaymentStatus


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        pass


# For Now all payment strategies are successful
class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiration_date: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date

    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} using credit card {self.card_number} with CVV {self.cvv} and expiration date {self.expiration_date}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, "Credit card payment successful")


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} using cash")
        return PaymentResult(amount, PaymentStatus.SUCCESS, "Cash payment successful")


class UPIPaymentStrategy(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} using upi id: {self.upi_id}")
        return PaymentResult(amount, PaymentStatus.SUCCESS, "UPI payment successful")
