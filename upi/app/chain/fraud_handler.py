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

    def __init__(self):
        super().__init__()
        # Create fraud-enhanced processor
        base_processor = ConcretePaymentProcessor()
        self.fraud_processor = FraudCheckDecorator(base_processor)

    def _process(self, payment: "Payment") -> StandardizedResponse:
        """
        Process payment through fraud-enhanced processor

        This handler:
        1. Delegates fraud checking to FraudCheckDecorator
        2. Handles chain flow control
        3. Maintains chain responsibility pattern
        """

        # Delegate to fraud-enhanced processor
        response = self.fraud_processor.process_payment(payment)

        # If fraud check failed, stop the chain
        if not response.success and response.status in ["FRAUD_DETECTED", "BLOCKED"]:
            return response

        # Fraud check passed, continue chain
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="FRAUD_CHECK_PASSED")
