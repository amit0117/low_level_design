from app.chain.base_handler import PaymentHandler
from app.adapters.base_adapter import StandardizedResponse
from app.models.enums import PaymentStatus, TransactionStatus
from app.models.transaction import Transaction
from app.models.npci_instance import NPCI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class SettlementHandler(PaymentHandler):
    """Handler for payment settlement and final processing"""

    def _process(self, payment: "Payment") -> StandardizedResponse:
        """Handle payment settlement with actual money transfer"""

        try:
            amount = payment.get_amount()
            payer_account = payment.get_payer_account()
            payee_account = payment.get_payee_account()

            if payer_account.get_balance() < amount:
                payment.set_status(PaymentStatus.FAILED)
                return StandardizedResponse(success=False, amount=amount, status="INSUFFICIENT_FUNDS")

            transaction = Transaction(payment)
            payment.add_transaction(transaction)

            npci = NPCI.get_instance()
            npci_response = npci.process_payment(
                payer_vpa=payer_account.get_vpa(), payee_vpa=payee_account.get_vpa(), amount=amount, payment_method=payment.get_payment_method()
            )

            if not npci_response.success:
                payment.set_status(PaymentStatus.FAILED)
                return StandardizedResponse(success=False, amount=amount, status="NPCI_FAILED")

            transaction.set_status(TransactionStatus.SUCCESS)

            payment.set_status(PaymentStatus.COMPLETED)

            return StandardizedResponse(success=True, amount=amount, status="SETTLED")

        except Exception as e:
            payment.set_status(PaymentStatus.FAILED)
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="SETTLEMENT_FAILED")
