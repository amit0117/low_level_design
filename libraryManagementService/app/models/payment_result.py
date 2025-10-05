from app.models.enums import PaymentStatus, PaymentMethod
from uuid import uuid4


class PaymentResult:
    def __init__(self, amount: float, status: PaymentStatus, payment_method: PaymentMethod):
        self.transaction_id = str(uuid4())
        self.amount = amount
        self.status = status
        self.payment_method = payment_method

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_amount(self) -> float:
        return self.amount

    def get_status(self) -> PaymentStatus:
        return self.status

    def get_payment_method(self) -> PaymentMethod:
        return self.payment_method

    def set_status(self, status: PaymentStatus):
        self.status = status

    def __str__(self) -> str:
        return f"Payment Result: Amount: {self.amount}, Status: {self.status}, Transaction ID: {self.transaction_id}"
