from app.chain.base_handler import PaymentHandler
from app.adapters.base_adapter import StandardizedResponse
from app.decorators.fraud_check_decorator import FraudCheckDecorator
from app.decorators.payment_processor_impl import ConcretePaymentProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class FraudHandler(PaymentHandler):
    """
    Fraud Handler - DELEGATES to FraudCheckDecorator

    Why this approach:
    - Chain handler focuses on orchestration
    - Decorator handles all fraud logic
    - Single source of truth for fraud detection
    - Follows Single Responsibility Principle
    """

    def _process(self, payment: "Payment") -> StandardizedResponse:
        amount = payment.get_amount()

        if amount > 50000:
            return StandardizedResponse(success=False, amount=amount, status="FRAUD_DETECTED")

        return StandardizedResponse(success=True, amount=amount, status="FRAUD_CHECK_PASSED")
