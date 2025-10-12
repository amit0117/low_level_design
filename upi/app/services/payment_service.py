from typing import TYPE_CHECKING
from app.chain.chain_factory import PaymentChainFactory
from app.adapters.base_adapter import StandardizedResponse

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentService:
    """Service layer for payment processing with chain"""

    def __init__(self):
        # Create payment processing chain using factory
        self.payment_chain = PaymentChainFactory.create_full_chain()

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process payment through chain"""
        return self.payment_chain.handle(payment)
