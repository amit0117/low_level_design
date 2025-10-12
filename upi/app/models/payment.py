from app.models.enums import PaymentStatus, PaymentMethod, Currency, PaymentType
from app.observers.payment_observer import PaymentSubject
from typing import TYPE_CHECKING, List
from uuid import uuid4
from datetime import datetime, timedelta
from threading import Timer

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.account import Account


class Payment(PaymentSubject):
    def __init__(
        self,
        payment_type: PaymentType,
        payment_method: PaymentMethod,
        amount: float,
        payer_account: "Account",
        payee_account: "Account",
        currency: Currency,
    ):
        super().__init__()
        self.payment_id = str(uuid4())
        self.payment_type = payment_type
        self.payment_method = payment_method
        self.amount = amount
        self.currency = currency
        self.status = PaymentStatus.PENDING
        self.payer_account: "Account" = payer_account
        self.payee_account: "Account" = payee_account
        self.created_at = datetime.now()
        self.transactions: List["Transaction"] = []  # Each payment can have multiple transactions, for retries, partial payments, etc.

        # Add payer as observer for payment status changes
        self.add_observer(payer_account.get_user())

        # Setup automatic expiry of payment after 3 seconds
        self.expiry_time = self.created_at + timedelta(seconds=3)
        self.expiry_timer = Timer(3.0, self.expire_payment)  # 3 seconds
        self.expiry_timer.start()

    def get_payment_id(self) -> str:
        return self.payment_id

    def get_payment_method(self) -> PaymentMethod:
        return self.payment_method

    def get_amount(self) -> float:
        return self.amount

    def get_status(self) -> PaymentStatus:
        return self.status

    def get_payer_account(self) -> "Account":
        return self.payer_account

    def get_payee_account(self) -> "Account":
        return self.payee_account

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_expiry_time(self) -> datetime:
        return self.expiry_time

    def is_expired(self) -> bool:
        return self.status == PaymentStatus.EXPIRED

    def add_transaction(self, transaction: "Transaction") -> None:
        """Add a transaction to this payment (for retries, partial payments)"""
        self.transactions.append(transaction)

    def get_transactions(self) -> List["Transaction"]:
        return self.transactions

    def get_latest_transaction(self) -> "Transaction":
        """Get the most recent transaction, or None if no transactions exist"""
        return self.transactions[-1] if self.transactions else None

    def set_status(self, status: PaymentStatus) -> None:
        """Update payment status and notify observers"""
        self.status = status
        self.notify_observers(self)

    def create_transaction(self) -> "Transaction":
        new_transaction = Transaction(self)
        self.add_transaction(new_transaction)
        return new_transaction

    def cancel_payment(self) -> None:
        """Cancel the payment and stop the expiry timer"""
        if self.expiry_timer.is_alive() and not self.is_expired():
            # only cancel the timer if it's alive and the payment is not expired
            self.expiry_timer.cancel()
            self.set_status(PaymentStatus.CANCELLED)

    def expire_payment(self) -> None:
        """Expire the payment if it's still pending"""
        if not self.is_expired():
            self.set_status(PaymentStatus.EXPIRED)
            print(f"Payment {self.payment_id} has expired")
        else:
            print(f"Payment {self.payment_id} has already expired")

    def extend_expiry(self, additional_minutes: int) -> None:
        """Extend the expiry time by additional minutes"""
        if self.is_expired():
            print(f"Payment {self.payment_id} has expired, cannot extend expiry")
            return
        if self.expiry_timer.is_alive():
            # Stop the timer if it's alive
            self.expiry_timer.cancel()

        self.expiry_time = datetime.now() + timedelta(minutes=additional_minutes)
        self.expiry_timer = Timer(additional_minutes * 60.0, self.expire_payment)
        self.expiry_timer.start()
        print(f"Payment {self.payment_id} expiry extended by {additional_minutes} minutes")
