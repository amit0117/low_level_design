from app.models.transactions.transaction import Transaction
from app.models.account import Account
from app.models.card import Card
from app.repositories.bank_repository import BankRepository


class BalanceInquiryTransaction(Transaction):
    def __init__(self, bank_name: str, account: Account, card: Card, pin: str):
        super().__init__()
        self.bank_name = bank_name
        self.bank_server = BankRepository.get_instance().get_bank_server(bank_name)
        self.account = account
        self.card = card
        self.pin = pin
        self._balance = None

        # Add user as observer for transaction notifications
        user = account.get_user()
        if user:
            self.add_observer(user)

    def validate(self) -> None:
        # Validate card
        if not self.bank_server.validate_card(self.card):
            raise ValueError("Invalid card")

        # Validate card expiration
        from datetime import datetime

        if self.card.get_expiration_date() < datetime.now():
            raise ValueError("Card has expired")

    def authorize(self) -> None:
        # Validate PIN
        if not self.bank_server.validate_pin(self.card, self.pin):
            raise ValueError("Invalid PIN")

        # Additional authorization checks can be added here

    def perform_transaction(self) -> None:
        # Fetch balance
        self._balance = self.bank_server.get_account_balance(self.account.get_account_number())

    def dispense_or_accept(self) -> None:
        # No physical action needed
        pass

    def print_receipt(self) -> None:
        print(f"Account balance for {self.account.get_account_number()}: {self._balance}")

    def _get_success_message(self) -> str:
        return f"Balance inquiry completed for account {self.account.get_account_number()}. Balance: ₹{self._balance}"

    def rollback(self) -> None:
        # Balance inquiry is read-only, no rollback needed
        pass
