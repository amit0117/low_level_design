from app.models.enums import PaymentStatus, PaymentMethod

from uuid import uuid4


class PaymentResponse:
    def __init__(self, status: PaymentStatus, payment_method: PaymentMethod):
        self.transaction_id = str(uuid4())
        self.status = status
        self.payment_method = payment_method

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_status(self) -> PaymentStatus:
        return self.status

    def get_payment_method(self) -> PaymentMethod:
        return self.payment_method
