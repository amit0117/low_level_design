from app.chain.base_handler import PaymentHandler
from app.adapters.base_adapter import StandardizedResponse
from app.proxies.secure_bank_proxy import SecureBankProxy
from app.decorators.payment_processor_impl import ConcretePaymentProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class AuthenticationHandler(PaymentHandler):
    """
    Authentication Handler - DELEGATES to SecureBankProxy

    Why this approach:
    - Chain handler focuses on orchestration
    - Proxy handles all authentication logic
    - Single source of truth for authentication
    - Follows Single Responsibility Principle
    """

    def __init__(self):
        super().__init__()
        # Create authentication-enhanced processor
        base_processor = ConcretePaymentProcessor()
        self.auth_processor = SecureBankProxy(base_processor)

    def _process(self, payment: "Payment") -> StandardizedResponse:
        """
        Process payment through authentication-enhanced processor

        This handler:
        1. Delegates authentication to SecureBankProxy
        2. Handles chain flow control
        3. Maintains chain responsibility pattern
        """

        # Delegate to authentication-enhanced processor
        response = self.auth_processor.process_payment(payment)

        # If authentication failed, stop the chain
        if not response.success and response.status in ["UNAUTHORIZED", "MAX_RETRIES_EXCEEDED"]:
            return response

        # Authentication passed, continue chain
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="AUTHENTICATED")
