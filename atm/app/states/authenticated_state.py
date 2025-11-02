from app.states.atm_state import ATMState
from app.models.enums import ATMStatus, TransactionType
from app.exceptions.insufficient_money import InsufficientCashException
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.atm import ATM


class AuthenticatedState(ATMState):
    """User has been authenticated, waiting for transaction selection"""

    def insert_card(self, atm, card) -> None:
        print("Card already inserted")

    def eject_card(self, atm) -> None:
        print("Card ejected")
        atm.current_card = None
        atm.current_pin = None
        atm.current_account = None
        atm.current_transaction_type = None
        atm.change_state(atm.idle_state)
        atm.set_status(ATMStatus.IDLE)

    def enter_pin(self, atm) -> None:
        print("Already authenticated")

    def select_transaction(self, atm: "ATM", txn_type: TransactionType) -> None:
        print(f"Transaction selected: {txn_type.value}")
        atm.current_transaction_type = txn_type
        atm.change_state(atm.transaction_selected_state)
        atm.set_status(ATMStatus.TRANSACTION_SELECTED)

        # For balance inquiry, no amount needed
        if txn_type == TransactionType.BALANCE_INQUIRY:
            self.perform_transaction(atm)

    def perform_transaction(self, atm, amount=None) -> None:
        print("Please select a transaction type first")
