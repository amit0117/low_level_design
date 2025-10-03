from app.models.enums import PaymentMethod, PaymentStatus
import uuid


class Payment:
    def __init__(self, amount: float, method: PaymentMethod, status: PaymentStatus) -> None:
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.method = method
        self.status = status

    def get_amount(self) -> float:
        return self.amount

    def get_method(self) -> PaymentMethod:
        return self.method

    def get_status(self) -> PaymentStatus:
        return self.status

    def get_id(self) -> str:
        return self.id

    def set_status(self, status: PaymentStatus) -> None:
        self.status = status
