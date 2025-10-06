from abc import ABC, abstractmethod
from app.models.payment_result import PaymentResult
from app.models.enums import PaymentStatus, PaymentMethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry_date: str) -> None:
        self.card_number = card_number
        self.cvv = cvv
        self.expiry_date = expiry_date

    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} with credit card")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CREDIT_CARD)


class DebitCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card_number: str) -> None:
        self.card_number = card_number

    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} with debit card")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.DEBIT_CARD)


class CashPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} with cash")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.CASH)


class BankTransferPaymentStrategy(PaymentStrategy):
    def __init__(self, account_number: str, bank_name: str) -> None:
        self.account_number = account_number
        self.bank_name = bank_name

    def pay(self, amount: float) -> PaymentResult:
        print(f"Paying {amount} with bank transfer")
        return PaymentResult(amount, PaymentStatus.SUCCESS, PaymentMethod.BANK_TRANSFER)
