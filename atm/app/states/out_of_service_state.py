from app.states.atm_state import ATMState
from app.models.enums import ATMStatus


class OutOfServiceState(ATMState):
    """ATM is out of service"""

    def insert_card(self, atm, card) -> None:
        print("ATM is out of service")

    def eject_card(self, atm) -> None:
        if hasattr(atm, "current_card") and atm.current_card:
            print("Card ejected")
            atm.current_card = None
        else:
            print("No card to eject")

    def enter_pin(self, atm) -> None:
        print("ATM is out of service")

    def select_transaction(self, atm, txn_type) -> None:
        print("ATM is out of service")

    def perform_transaction(self, atm, amount=None) -> None:
        print("ATM is out of service")
