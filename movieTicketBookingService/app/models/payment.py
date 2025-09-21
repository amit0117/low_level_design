from app.models.enums import PaymentStatus
import uuid


class PaymentResult:
    def __init__(self, amount: float, status: PaymentStatus, message: str = ""):
        self._id = str(uuid.uuid4())
        self._amount = amount
        self._status = status
        self._message = message

    @property
    def id(self) -> str:
        return self._id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def status(self) -> PaymentStatus:
        return self._status

    @property
    def message(self) -> str:
        return self._message
