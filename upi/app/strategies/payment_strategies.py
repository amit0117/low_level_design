from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.adapters.base_adapter import StandardizedResponse
from app.models.enums import PaymentMethod

if TYPE_CHECKING:
    from app.models.payment import Payment


class PaymentStrategy(ABC):
    """Base strategy interface for different payment methods"""

    @abstractmethod
    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process payment using specific strategy"""
        raise NotImplementedError

    @abstractmethod
    def get_payment_method(self) -> PaymentMethod:
        """Get the payment method this strategy handles"""
        raise NotImplementedError


class UPIPushStrategy(PaymentStrategy):
    """Strategy for UPI Push payments"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process UPI Push payment"""
        # UPI Push: Payer initiates payment to payee
        # Direct debit from payer's account

        payer_vpa = payment.get_payer_account().get_vpa()
        payee_vpa = payment.get_payee_account().get_vpa()
        amount = payment.get_amount()

        # Simulate UPI Push processing
        # In real implementation, this would call UPI/NPCI APIs

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.UPI_PUSH


class UPIPullStrategy(PaymentStrategy):
    """Strategy for UPI Pull payments (Collect requests)"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process UPI Pull payment"""
        # UPI Pull: Payee requests money from payer
        # Requires payer approval

        payer_vpa = payment.get_payer_account().get_vpa()
        payee_vpa = payment.get_payee_account().get_vpa()
        amount = payment.get_amount()

        # Simulate UPI Pull processing
        # In real implementation, this would:
        # 1. Send collect request to payer
        # 2. Wait for payer approval
        # 3. Process payment if approved

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.UPI_PULL


class CreditCardStrategy(PaymentStrategy):
    """Strategy for Credit Card payments"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process Credit Card payment"""
        # Credit Card: Process through card network

        amount = payment.get_amount()

        # Simulate credit card processing
        # In real implementation, this would:
        # 1. Validate card details
        # 2. Check credit limit
        # 3. Process through card network (Visa/MasterCard)
        # 4. Handle 3D Secure if required

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.CREDIT_CARD


class DebitCardStrategy(PaymentStrategy):
    """Strategy for Debit Card payments"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process Debit Card payment"""
        # Debit Card: Direct debit from bank account

        amount = payment.get_amount()

        # Simulate debit card processing
        # In real implementation, this would:
        # 1. Validate card details
        # 2. Check account balance
        # 3. Process through card network
        # 4. Handle PIN verification

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.DEBIT_CARD


class NetBankingStrategy(PaymentStrategy):
    """Strategy for Net Banking payments"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process Net Banking payment"""
        # Net Banking: Direct bank transfer

        amount = payment.get_amount()

        # Simulate net banking processing
        # In real implementation, this would:
        # 1. Redirect to bank's net banking portal
        # 2. Handle user authentication
        # 3. Process transfer
        # 4. Handle callback/redirect

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.NET_BANKING


class WalletStrategy(PaymentStrategy):
    """Strategy for Wallet payments"""

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Process Wallet payment"""
        # Wallet: Deduct from digital wallet balance

        amount = payment.get_amount()

        # Simulate wallet processing
        # In real implementation, this would:
        # 1. Check wallet balance
        # 2. Deduct amount from wallet
        # 3. Update wallet balance
        # 4. Process to payee

        return StandardizedResponse(success=True, amount=amount, status="SUCCESS")

    def get_payment_method(self) -> PaymentMethod:
        return PaymentMethod.WALLET
