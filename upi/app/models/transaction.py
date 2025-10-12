from app.models.enums import TransactionStatus
from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING
from app.observers.transaction_observer import TransactionSubject
from app.states.transaction_state import TransactionState, PendingState

if TYPE_CHECKING:
    from app.models.payment import Payment


class Transaction(TransactionSubject):
    def __init__(
        self,
        payment: "Payment",
    ):
        super().__init__()  # Initialize TransactionSubject
        self.transaction_id = str(uuid4())
        self.transaction_status: TransactionStatus = TransactionStatus.PENDING
        self.transaction_state: TransactionState = PendingState()
        self.timestamp = datetime.now()
        self.payment: "Payment" = payment
        # add both payer and payee as observers
        self.add_observer(payment.get_payer_account().get_user())
        self.add_observer(payment.get_payee_account().get_user())
        # Add this transaction to the account of the payer and on the completion of this transaction, we will add this transaction to the account of the payee
        payment.get_payer_account().add_transaction(self)

    def get_transaction_id(self) -> str:
        return self.transaction_id

    def get_transaction_amount(self) -> float:
        return self.payment.get_amount()

    def get_payment(self) -> "Payment":
        return self.payment

    def get_transaction_status(self) -> TransactionStatus:
        return self.transaction_status

    def set_status(self, status: TransactionStatus) -> None:
        # If the transaction is successful, we need to add this transaction to the account of the payee
        if status == TransactionStatus.SUCCESS:
            # Add this transaction to the account of the payee IF the transaction is successful
            self.payment.get_payee_account().add_transaction(self)
        self.transaction_status = status
        self.notify_observers(self)

    def set_state(self, state: TransactionState) -> None:
        self.transaction_state = state

    def cancel(self) -> bool:
        return self.transaction_state.cancel(self)

    def refund(self) -> bool:
        return self.transaction_state.refund(self)

    def process(self) -> bool:
        return self.transaction_state.process(self)
