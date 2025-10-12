from abc import ABC, abstractmethod
from app.adapters.base_adapter import StandardizedResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentProcessor(ABC):
    """Base interface for payment processing"""

    @abstractmethod
    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        raise NotImplementedError


class PaymentProcessorProxy(PaymentProcessor):
    """Base proxy for payment processors - handles access control"""

    def __init__(self, processor: PaymentProcessor):
        self._processor = processor

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        return self._processor.process_payment(payment)
