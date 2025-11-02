from app.states.atm_state import ATMState
from app.models.enums import ATMStatus, TransactionType
from typing import Optional
from typing import TYPE_CHECKING
from app.models.card import Card

if TYPE_CHECKING:
    from app.models.atm import ATM


class TransactionSelectedState(ATMState):
    """Transaction type has been selected, ready to perform transaction"""

    def insert_card(self, atm: "ATM", card: Card) -> None:
        print("Card already inserted")

    def eject_card(self, atm: "ATM") -> None:
        print("Transaction cancelled. Card ejected")
        self._reset_atm(atm)

    def enter_pin(self, atm: "ATM") -> None:
        print("Already authenticated")

    def select_transaction(self, atm: "ATM", txn_type: TransactionType) -> None:
        print(f"Transaction changed to: {txn_type.value}")
        atm.current_transaction_type = txn_type

    def perform_transaction(self, atm: "ATM", amount: Optional[float] = None) -> None:
        if not atm.current_transaction_type:
            print("Error: No transaction selected")
            return

        if atm.current_transaction_type in [TransactionType.WITHDRAWAL, TransactionType.DEPOSIT, TransactionType.TRANSFER] and amount is None:
            print("Error: Amount required for this transaction")
            return

        atm.change_state(atm.transaction_processing_state)
        atm.set_status(ATMStatus.TRANSACTION_PROCESSING)

        try:
            if atm.current_transaction_type == TransactionType.WITHDRAWAL:
                self._perform_withdrawal(atm, amount)
            elif atm.current_transaction_type == TransactionType.DEPOSIT:
                self._perform_deposit(atm, amount)
            elif atm.current_transaction_type == TransactionType.TRANSFER:
                print("Transfer transaction requires additional details")
                # In a real system, would prompt for destination account
            elif atm.current_transaction_type == TransactionType.BALANCE_INQUIRY:
                self._perform_balance_inquiry(atm)

            # After transaction, return to authenticated state or eject card
            atm.change_state(atm.authenticated_state)
            atm.set_status(ATMStatus.AUTHENTICATED)
            atm.current_transaction_type = None

        except Exception as e:
            print(f"Transaction failed: {e}")
            atm.change_state(atm.authenticated_state)
            atm.set_status(ATMStatus.AUTHENTICATED)

    def _perform_withdrawal(self, atm: "ATM", amount: float) -> None:
        if not atm.current_account:
            print("Error: Account not found")
            return
        bank_name = atm.current_account.get_bank_name()
        atm.withdraw(bank_name, atm.current_account, amount, atm.current_card, atm.current_pin)

    def _perform_deposit(self, atm: "ATM", amount: float) -> None:
        if not atm.current_account:
            print("Error: Account not found")
            return
        bank_name = atm.current_account.get_bank_name()
        atm.deposit(bank_name, atm.current_account, amount, atm.current_card, atm.current_pin)

    def _perform_balance_inquiry(self, atm: "ATM") -> None:
        if not atm.current_account:
            print("Error: Account not found")
            return
        bank_name = atm.current_account.get_bank_name()
        atm.check_balance(bank_name, atm.current_account, atm.current_card, atm.current_pin)

    def _validate_cash_availability(self, atm: "ATM", amount: float) -> bool:
        """Validate if cash dispenser has sufficient cash"""
        if amount is None or amount <= 0:
            return False
        return atm.cash_dispenser.has_sufficient_cash(int(amount))

    def _reset_atm(self, atm: "ATM") -> None:
        atm.current_card = None
        atm.current_pin = None
        atm.current_account = None
        atm.current_transaction_type = None
        atm.change_state(atm.idle_state)
        atm.set_status(ATMStatus.IDLE)
