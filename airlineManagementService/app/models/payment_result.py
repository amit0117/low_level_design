from app.models.enums import PaymentStatus, PaymentMethod
from uuid import uuid4
from datetime import datetime


class PaymentResult:
    def __init__(self, amount: float, payment_status: PaymentStatus, payment_method: PaymentMethod):
        self.transaction_id = str(uuid4())
        self.amount = amount
        self.created_at = datetime.now()
        self.payment_status = payment_status
        self.payment_method = payment_method

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_payment_status(self) -> PaymentStatus:
        return self.payment_status

    def get_payment_method(self) -> PaymentMethod:
        return self.payment_method

    def get_amount(self) -> float:
        return self.amount

    def get_created_at(self) -> datetime:
        return self.created_at
