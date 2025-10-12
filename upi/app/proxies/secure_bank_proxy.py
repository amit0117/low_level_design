from typing import Dict, Any
from app.proxies.base_proxy import PaymentProcessorProxy, PaymentProcessor
from app.adapters.base_adapter import StandardizedResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class SecureBankProxy(PaymentProcessorProxy):
    """
    Secure Bank Proxy - SECURITY & ACCESS CONTROL

    Why Proxy Pattern:
    - Controls access to sensitive bank APIs
    - Enforces authentication and authorization
    - Handles retries and error recovery
    - Acts as security gateway
    """

    def __init__(self, processor: PaymentProcessor):
        super().__init__(processor)
        self.authenticated_sessions = set()
        self.max_retries = 3

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Secure payment processing with authentication and retries"""

        # Authentication check
        if not self._is_authenticated(payment):
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="UNAUTHORIZED")

        # Retry logic for failed requests
        for attempt in range(self.max_retries):
            response = self._processor.process_payment(payment)

            if response.success:
                return response

            # Log failed attempt
            if attempt < self.max_retries - 1:
                continue  # Retry

        return StandardizedResponse(success=False, amount=payment.get_amount(), status="MAX_RETRIES_EXCEEDED")

    def _is_authenticated(self, payment: "Payment") -> bool:
        """Check if payment request is authenticated"""
        # In real implementation, check JWT tokens, API keys, etc.
        payer_vpa = payment.get_payer_account().get_vpa()
        return payer_vpa in self.authenticated_sessions or self._authenticate_user(payer_vpa)

    def _authenticate_user(self, vpa: str) -> bool:
        """Authenticate user and add to session"""
        # Simulate authentication
        self.authenticated_sessions.add(vpa)
        return True
