from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.adapters.base_adapter import StandardizedResponse

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentProcessor(ABC):
    """Base interface for payment processing"""

    @abstractmethod
    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process payment and return standardized response"""
        raise NotImplementedError("process_payment method must be implemented")


class PaymentProcessorDecorator(PaymentProcessor):
    """Base decorator for payment processors"""

    def __init__(self, processor: PaymentProcessor):
        self._processor = processor

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Delegate to wrapped processor"""
        return self._processor.process_payment(payment)
