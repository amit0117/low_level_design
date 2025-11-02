from app.models.transactions.transaction import Transaction
from app.models.account import Account
from app.models.card import Card
from app.repositories.bank_repository import BankRepository
from app.exceptions.insufficient_money import InsufficientFundsException


class TransferTransaction(Transaction):
    def __init__(
        self,
        source_bank_name: str,
        destination_bank_name: str,
        source_account: Account,
        destination_account: Account,
        amount: float,
        card: Card,
        pin: str,
    ):
        super().__init__()
        self.source_bank_name = source_bank_name
        self.destination_bank_name = destination_bank_name
        self.source_bank_server = BankRepository.get_instance().get_bank_server(source_bank_name)
        self.destination_bank_server = BankRepository.get_instance().get_bank_server(destination_bank_name)
        self.source_account = source_account
        self.destination_account = destination_account
        self.amount = amount
        self.card = card
        self.pin = pin
        self._debit_performed = False
        self._credit_performed = False

        # Add both sender and receiver as observers for transfer transactions
        source_user = source_account.get_user()
        destination_user = destination_account.get_user()
        if source_user:
            self.add_observer(source_user)
        if destination_user and destination_user != source_user:
            self.add_observer(destination_user)

    def validate(self) -> None:
        # Validate card
        if not self.source_bank_server.validate_card(self.card):
            raise ValueError("Invalid card")

        # Validate card expiration
        from datetime import datetime

        if self.card.get_expiration_date() < datetime.now():
            raise ValueError("Card has expired")

        # Validate amount
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate source account balance
        if self.source_bank_server.get_account_balance(self.source_account.get_account_number()) < self.amount:
            raise InsufficientFundsException("Insufficient funds in source account")

    def authorize(self) -> None:
        # Validate PIN
        if not self.source_bank_server.validate_pin(self.card, self.pin):
            raise ValueError("Invalid PIN")

        # Additional authorization checks can be added here

    def perform_transaction(self) -> None:
        # Perform debit first
        self.source_bank_server.withdraw(self.source_account.get_account_number(), self.amount)
        self._debit_performed = True
        try:
            # Then perform credit
            self.destination_bank_server.deposit(self.destination_account.get_account_number(), self.amount)
            self._credit_performed = True
        except Exception as e:
            # If credit fails, rollback debit
            self.source_bank_server.deposit(self.source_account.get_account_number(), self.amount)
            self._debit_performed = False
            raise e

    def dispense_or_accept(self) -> None:
        # No physical cash movement for transfer
        print(f"Transfer processed: {self.amount} from {self.source_account.get_account_number()} to {self.destination_account.get_account_number()}")

    def print_receipt(self) -> None:
        print(
            f"Transfer successful: {self.amount} transferred from account {self.source_account.get_account_number()} to {self.destination_account.get_account_number()}"
        )

    def _get_success_message(self) -> str:
        return f"Transfer successful: ₹{self.amount} transferred from account {self.source_account.get_account_number()} to {self.destination_account.get_account_number()}"

    def rollback(self) -> None:
        if self._credit_performed:
            # Revert credit
            self.destination_bank_server.withdraw(self.destination_account.get_account_number(), self.amount)
            self._credit_performed = False
        if self._debit_performed:
            # Revert debit
            self.source_bank_server.deposit(self.source_account.get_account_number(), self.amount)
            self._debit_performed = False
