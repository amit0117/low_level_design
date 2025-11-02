from app.states.atm_state import ATMState
from app.models.enums import ATMStatus
from app.models.card import Card


class IdleState(ATMState):
    """ATM is idle and waiting for a card to be inserted"""

    def insert_card(self, atm, card: Card) -> None:
        print("Card inserted")
        atm.current_card = card
        atm.change_state(atm.card_inserted_state)
        atm.set_status(ATMStatus.CARD_INSERTED)

    def eject_card(self, atm) -> None:
        print("No card to eject")

    def enter_pin(self, atm) -> None:
        print("Please insert card first")

    def select_transaction(self, atm, txn_type) -> None:
        print("Please insert card and authenticate first")

    def perform_transaction(self, atm, amount=None) -> None:
        print("Please insert card and authenticate first")
