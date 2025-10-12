from app.chain.base_handler import PaymentHandler
from app.adapters.base_adapter import StandardizedResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class ValidationHandler(PaymentHandler):
    """Handler for payment validation"""

    def _process(self, payment: "Payment") -> StandardizedResponse:
        """Validate payment request"""

        # Check if payment is expired
        if payment.is_expired():
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="EXPIRED")

        # Validate amount
        if payment.get_amount() <= 0:
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="INVALID_AMOUNT")

        # Validate accounts
        if not payment.get_payer_account() or not payment.get_payee_account():
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="INVALID_ACCOUNTS")

        # Validate VPAs
        payer_vpa = payment.get_payer_account().get_vpa()
        payee_vpa = payment.get_payee_account().get_vpa()

        if not payer_vpa or not payee_vpa:
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="INVALID_VPA")

        # Same account check
        if payer_vpa == payee_vpa:
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="SAME_ACCOUNT")

        # Validation passed
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="VALIDATED")
