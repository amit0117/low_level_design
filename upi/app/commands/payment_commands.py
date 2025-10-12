from typing import TYPE_CHECKING, Optional
from app.commands.base_command import Command
from app.models.enums import CommandStatus, TransactionStatus, PaymentMethod
from app.exceptions.insufficient_fund import InsufficientFundsException
from app.models.npci_instance import NPCI

if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.transaction import Transaction


class ExecutePaymentCommand(Command):
    """Command to execute payment through NPCI"""

    def __init__(self, payment: "Payment"):
        super().__init__()
        self.payment = payment
        self.transaction: Optional["Transaction"] = None
        self.npci_instance = NPCI.get_instance()

    def execute(self) -> bool:
        try:
            self.set_status(CommandStatus.EXECUTING)

            # Create transaction
            self.transaction = self.payment.create_transaction()

            # Process payment through chain (includes validation, authentication, fraud check, routing, settlement)
            success = self._process_payment_through_chain()

            # Only update local account balance if processing is successful
            if success:
                self._update_local_account_balances()

            return success

        except Exception as e:
            self.set_error(str(e))
            return False

    def _process_payment_through_chain(self) -> bool:
        """Process payment through the complete chain (validation, auth, fraud, routing, settlement)"""

        # Process payment through NPCI (which uses the chain internally)
        payer_vpa = self.payment.get_payer_account().get_vpa()
        payee_vpa = self.payment.get_payee_account().get_vpa()
        amount = self.payment.get_amount()
        payment_method = self.payment.get_payment_method()

        response = self.npci_instance.process_payment(payer_vpa=payer_vpa, payee_vpa=payee_vpa, amount=amount, payment_method=payment_method)

        if response.success:
            # Payment processed successfully through chain
            self.transaction.set_status(TransactionStatus.SUCCESS)
            self.payment.set_status(self.payment.get_status().APPROVED)

            # Store transaction reference for audit trail
            self.transaction.npci_reference = f"NPCI_{self.transaction.get_transaction_id()}"

            return True
        else:
            self.set_error("Payment processing failed")
            return False

    def _update_local_account_balances(self) -> None:
        """Update local account balances to reflect NPCI's successful transaction"""
        try:
            payer_account = self.payment.get_payer_account()
            payee_account = self.payment.get_payee_account()
            amount = self.payment.get_amount()

            # Update local balances to match NPCI's successful transaction
            payer_account.withdraw(amount)
            payee_account.deposit(amount)

            # Add transaction to account history
            payer_account.add_transaction(self.transaction)
            payee_account.add_transaction(self.transaction)

            self.set_status(CommandStatus.COMPLETED)

        except Exception as e:
            self.set_error(f"Failed to update local account balances: {str(e)}")

    def _reverse_local_account_balances(self) -> None:
        """Reverse local account balances for rollback/refund"""
        try:
            payer_account = self.payment.get_payer_account()
            payee_account = self.payment.get_payee_account()
            amount = self.payment.get_amount()

            # Reverse the transaction: credit payer, debit payee
            payer_account.deposit(amount)
            payee_account.withdraw(amount)

        except Exception as e:
            self.set_error(f"Failed to reverse local account balances: {str(e)}")

    def undo(self) -> bool:
        """Rollback the payment through NPCI"""
        self.set_status(CommandStatus.EXECUTING)
        if not self.transaction or self.transaction.get_transaction_status() != TransactionStatus.SUCCESS:
            self.set_error("Cannot rollback non-successful transaction")
            return False

        try:
            # Process refund through NPCI
            payer_vpa = self.payment.get_payer_account().get_vpa()
            payee_vpa = self.payment.get_payee_account().get_vpa()

            npci_response = self.npci_instance.process_refund(
                original_transaction_id=self.transaction.get_transaction_id(),
                amount=self.payment.get_amount(),
                payer_vpa=payer_vpa,
                payee_vpa=payee_vpa,
            )

            if npci_response.success:
                # NPCI has already handled the actual refund between banks
                # We need to reverse the local account balances
                self._reverse_local_account_balances()

                # Update transaction and payment status
                self.transaction.cancel()
                self.payment.set_status(self.payment.get_status().CANCELLED)
                self.set_status(CommandStatus.COMPLETED)
                return True
            else:
                self.set_error("NPCI refund failed")
                return False

        except Exception as e:
            self.set_error(f"Rollback failed: {str(e)}")
            return False

    def can_retry(self) -> bool:
        return super().can_retry() and not self.payment.is_expired()


class RefundCommand(Command):
    """Command to process refund through NPCI"""

    def __init__(self, transaction: "Transaction"):
        super().__init__()
        self.transaction = transaction
        self.original_payment = transaction.get_payment()
        self.npci_instance = NPCI.get_instance()

    def execute(self) -> bool:
        try:
            self.set_status(CommandStatus.EXECUTING)

            if self.transaction.get_transaction_status() != TransactionStatus.SUCCESS:
                self.set_error("Can only refund successful transactions")
                return False

            # Process refund through NPCI
            payer_vpa = self.original_payment.get_payer_account().get_vpa()
            payee_vpa = self.original_payment.get_payee_account().get_vpa()

            npci_response = self.npci_instance.process_refund(
                original_transaction_id=self.transaction.get_transaction_id(),
                amount=self.original_payment.get_amount(),
                payer_vpa=payer_vpa,
                payee_vpa=payee_vpa,
            )

            if npci_response.success:
                # NPCI has already handled the actual refund between banks
                # We need to reverse the local account balances
                self._reverse_local_account_balances()

                # Update transaction status
                self.transaction.refund()
                self.set_status(CommandStatus.COMPLETED)
                return True
            else:
                self.set_error("NPCI refund failed")
                return False

        except Exception as e:
            self.set_error(str(e))
            return False

    def _reverse_local_account_balances(self) -> None:
        """Reverse local account balances for refund"""
        try:
            payer_account = self.original_payment.get_payer_account()
            payee_account = self.original_payment.get_payee_account()
            amount = self.original_payment.get_amount()

            # Reverse the original transaction: credit payer, debit payee
            payer_account.deposit(amount)
            payee_account.withdraw(amount)

        except Exception as e:
            self.set_error(f"Failed to reverse local account balances: {str(e)}")

    def undo(self) -> bool:
        """Undo refund - re-apply the payment"""
        if self.transaction.get_transaction_status() != TransactionStatus.REFUNDED:
            return False

        try:
            # For undo refund, we would need to process a new payment through NPCI
            # This is complex and usually not allowed in real UPI systems
            self.set_error("Undo refund not supported - would require new payment processing")
            return False
        except Exception as e:
            self.set_error(f"Undo refund failed: {str(e)}")
            return False

    def can_retry(self) -> bool:
        return super().can_retry()
