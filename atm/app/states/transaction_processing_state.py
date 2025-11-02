from app.states.atm_state import ATMState
from app.models.enums import ATMStatus
from typing import TYPE_CHECKING
from app.models.card import Card

if TYPE_CHECKING:
    from app.models.atm import ATM


class TransactionProcessingState(ATMState):
    """ATM is currently processing a transaction"""

    def insert_card(self, atm: "ATM", card: Card) -> None:
        print("Transaction in progress. Please wait")

    def eject_card(self, atm: "ATM") -> None:
        print("Cannot eject card during transaction processing")

    def enter_pin(self, atm: "ATM") -> None:
        print("Transaction in progress. Please wait")

    def select_transaction(self, atm: "ATM", txn_type) -> None:
        print("Transaction in progress. Please wait")

    def perform_transaction(self, atm: "ATM", amount=None) -> None:
        print("Transaction already in progress. Please wait")
