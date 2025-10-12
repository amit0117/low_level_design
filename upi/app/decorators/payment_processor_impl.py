from app.decorators.base_decorator import PaymentProcessor
from app.adapters.base_adapter import StandardizedResponse
from app.models.npci_instance import NPCI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class ConcretePaymentProcessor(PaymentProcessor):
    """Concrete implementation of payment processor using NPCI"""

    def __init__(self):
        self.npci_instance = NPCI.get_instance()

    def process_payment(self, payment) -> StandardizedResponse:
        """Process payment through NPCI"""

        payer_vpa = payment.get_payer_account().get_vpa()
        payee_vpa = payment.get_payee_account().get_vpa()
        amount = payment.get_amount()
        payment_method = payment.get_payment_method()

        # Process payment through NPCI
        return self.npci_instance.process_payment(payer_vpa=payer_vpa, payee_vpa=payee_vpa, amount=amount, payment_method=payment_method)
