from app.models.transactions.transaction import Transaction
from app.models.account import Account
from app.models.card import Card
from app.repositories.bank_repository import BankRepository


class DepositTransaction(Transaction):
    def __init__(self, bank_name: str, account: Account, amount: float, card: Card, pin: str):
        super().__init__()
        self.bank_name = bank_name
        self.bank_server = BankRepository.get_instance().get_bank_server(bank_name)
        self.account = account
        self.amount = amount
        self.card = card
        self.pin = pin
        self._transaction_performed = False

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

        # Validate amount
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

    def authorize(self) -> None:
        # Validate PIN
        if not self.bank_server.validate_pin(self.card, self.pin):
            raise ValueError("Invalid PIN")

        # Additional authorization checks can be added here

    def perform_transaction(self) -> None:
        try:
            self.bank_server.deposit(self.account.get_account_number(), self.amount)
            self._transaction_performed = True
        except Exception as e:
            raise e

    def dispense_or_accept(self) -> None:
        # Accept cash/cheque from user (in real system, physical mechanism)
        print(f"Accepting deposit of {self.amount}")

    def print_receipt(self) -> None:
        print(f"Deposit successful: {self.amount} to account {self.account.get_account_number()}")

    def _get_success_message(self) -> str:
        return f"Deposit successful: ₹{self.amount} deposited to account {self.account.get_account_number()}"

    def rollback(self) -> None:
        if self._transaction_performed:
            # Revert the bank transaction
            self.bank_server.withdraw(self.account.get_account_number(), self.amount)
            self._transaction_performed = False
