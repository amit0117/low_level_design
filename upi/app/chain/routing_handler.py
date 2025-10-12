from app.chain.base_handler import PaymentHandler
from app.adapters.base_adapter import StandardizedResponse
from app.models.enums import PaymentMethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class RoutingHandler(PaymentHandler):
    """Handler for payment routing and processing"""

    def _process(self, payment: "Payment") -> StandardizedResponse:
        """Route payment based on payment method"""

        payment_method = payment.get_payment_method()
        amount = payment.get_amount()

        try:
            # Route based on payment method
            if payment_method == PaymentMethod.UPI_PUSH:
                return self._process_upi_push(payment)
            elif payment_method == PaymentMethod.UPI_PULL:
                return self._process_upi_pull(payment)
            elif payment_method == PaymentMethod.CREDIT_CARD:
                return self._process_credit_card(payment)
            elif payment_method == PaymentMethod.DEBIT_CARD:
                return self._process_debit_card(payment)
            elif payment_method == PaymentMethod.NET_BANKING:
                return self._process_net_banking(payment)
            elif payment_method == PaymentMethod.WALLET:
                return self._process_wallet(payment)
            else:
                return StandardizedResponse(success=False, amount=amount, status="UNSUPPORTED_PAYMENT_METHOD")

        except Exception as e:
            return StandardizedResponse(success=False, amount=amount, status="ROUTING_ERROR")

    def _process_upi_push(self, payment: "Payment") -> StandardizedResponse:
        """Process UPI Push payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="UPI_PUSH_SUCCESS")

    def _process_upi_pull(self, payment: "Payment") -> StandardizedResponse:
        """Process UPI Pull payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="UPI_PULL_SUCCESS")

    def _process_credit_card(self, payment: "Payment") -> StandardizedResponse:
        """Process Credit Card payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="CREDIT_CARD_SUCCESS")

    def _process_debit_card(self, payment: "Payment") -> StandardizedResponse:
        """Process Debit Card payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="DEBIT_CARD_SUCCESS")

    def _process_net_banking(self, payment: "Payment") -> StandardizedResponse:
        """Process Net Banking payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="NET_BANKING_SUCCESS")

    def _process_wallet(self, payment: "Payment") -> StandardizedResponse:
        """Process Wallet payment"""
        return StandardizedResponse(success=True, amount=payment.get_amount(), status="WALLET_SUCCESS")
