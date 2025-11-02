from app.models.transactions.transaction import Transaction
from app.models.account import Account
from app.models.cash_dispenser import CashDispenser
from app.models.card import Card
from app.repositories.bank_repository import BankRepository
from app.exceptions.insufficient_money import InsufficientFundsException, InsufficientCashException


class WithdrawalTransaction(Transaction):
    def __init__(self, bank_name: str, account: Account, amount: float, cash_dispenser: CashDispenser, card: Card, pin: str):
        super().__init__()
        self.bank_name = bank_name
        self.bank_server = BankRepository.get_instance().get_bank_server(bank_name)
        self.account = account
        self.amount = amount
        self.cash_dispenser = cash_dispenser
        self.card = card
        self.pin = pin
        self._dispensed = False
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

        # Validate account balance
        if self.bank_server.get_account_balance(self.account.get_account_number()) < self.amount:
            raise InsufficientFundsException("Insufficient funds in account")

        # Validate ATM cash availability
        if not self.cash_dispenser.has_sufficient_cash(int(self.amount)):
            raise InsufficientCashException("ATM has insufficient cash")

    def authorize(self) -> None:
        # Validate PIN
        if not self.bank_server.validate_pin(self.card, self.pin):
            raise ValueError("Invalid PIN")

        # Additional authorization checks can be added here

    def perform_transaction(self) -> None:
        self.bank_server.withdraw(self.account.get_account_number(), self.amount)
        self._transaction_performed = True

    def dispense_or_accept(self) -> None:
        self.cash_dispenser.dispense_cash(int(self.amount))
        self._dispensed = True

    def print_receipt(self) -> None:
        print(f"Withdrawal successful: {self.amount} from account {self.account.get_account_number()}")

    def _get_success_message(self) -> str:
        return f"Withdrawal successful: ₹{self.amount} withdrawn from account {self.account.get_account_number()}"

    def rollback(self) -> None:
        if self._transaction_performed:
            # Revert the bank transaction
            self.bank_server.deposit(self.account.get_account_number(), self.amount)
            self._transaction_performed = False
        # Note: Physical cash rollback is not trivial in real systems
