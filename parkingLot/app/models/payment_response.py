from app.models.enums import PaymentStatus, PaymentMethod
from uuid import uuid4


class PaymentResponse:
    def __init__(self, amount: float, payment_method: PaymentMethod, status: PaymentStatus):
        self.transaction_id = str(uuid4())
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_amount(self) -> float:
        return self.amount

    def get_payment_method(self) -> PaymentMethod:
        return self.payment_method

    def get_status(self) -> PaymentStatus:
        return self.status

    def update_status(self, status: PaymentStatus) -> None:
        self.status = status
