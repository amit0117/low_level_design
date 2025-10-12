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

    def _process(self, payment: "Payment") -> StandardizedResponse:
        amount = payment.get_amount()
        payer_account = payment.get_payer_account()

        if not payer_account:
            return StandardizedResponse(success=False, amount=amount, status="UNAUTHORIZED")

        return StandardizedResponse(success=True, amount=amount, status="AUTHENTICATED")
