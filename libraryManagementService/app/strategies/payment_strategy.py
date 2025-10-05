from abc import ABC, abstractmethod
from app.models.enums import PaymentStatus, PaymentMethod
from app.models.payment_result import PaymentResult


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> "PaymentResult":
        raise NotImplementedError("Subclasses must implement this method")


# For now assuming all payments are successful
class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> "PaymentResult":
        print(f"Processing credit card payment of {amount} with card {self.card_number} and cvv {self.cvv}\n")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CREDIT_CARD)


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> "PaymentResult":
        print(f"Processing cash payment of {amount}\n")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CASH)


class BankTransferPaymentStrategy(PaymentStrategy):
    def __init__(self, account_number: str, bank_name: str):
        self.account_number = account_number
        self.bank_name = bank_name

    def pay(self, amount: float) -> "PaymentResult":
        print(f"Processing bank transfer payment of {amount} to {self.account_number} from {self.bank_name}\n")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.BANK_TRANSFER)
