from app.states.atm_state import ATMState
from app.models.enums import ATMStatus
from app.models.card import Card


class CardInsertedState(ATMState):
    """Card has been inserted, waiting for PIN entry"""

    def insert_card(self, atm, card: Card) -> None:
        print("Card already inserted. Please eject card first")

    def eject_card(self, atm) -> None:
        print("Card ejected")
        atm.current_card = None
        atm.current_pin = None
        atm.current_account = None
        atm.current_transaction_type = None
        atm.change_state(atm.idle_state)
        atm.set_status(ATMStatus.IDLE)

    def enter_pin(self, atm) -> None:
        if not atm.current_card:
            print("Error: No card present")
            return

        # Use keypad to read PIN from user
        with atm.keypad:
            atm.keypad.enter_pin()
            pin = atm.keypad.get_pin()

        if not pin:
            print("Error: No PIN entered")
            return

        print(f"PIN entered: {'*' * len(pin)}")

        # Validate card and PIN using bank server
        if not atm.bank_server.validate_card(atm.current_card):
            print("Invalid card")
            self.eject_card(atm)
            return

        if not atm.bank_server.validate_pin(atm.current_card, pin):
            print("Invalid PIN")
            self.eject_card(atm)
            return

        print("PIN validated successfully")
        atm.current_pin = pin

        # Get account from card (in real system, this would be fetched from bank)
        # For now, we'll need to pass account through context or fetch it
        # This is a placeholder - in a real implementation, the account would be retrieved
        # based on the card number through the bank server
        atm.change_state(atm.authenticated_state)
        atm.set_status(ATMStatus.AUTHENTICATED)

    def select_transaction(self, atm, txn_type) -> None:
        print("Please enter PIN first")

    def perform_transaction(self, atm, amount=None) -> None:
        print("Please enter PIN and select transaction first")
