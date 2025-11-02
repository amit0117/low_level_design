from app.models.bank_server import BankServer
from app.models.banks.icici_bank import ICICIBank
from app.models.card import Card
from app.exceptions.insufficient_money import InsufficientFundsException


class ICICIBankAdapter(BankServer):
    """
    Adapter for ICICI Bank
    Translates BankServer interface to ICICI proprietary API
    """

    def __init__(self, icici_bank: ICICIBank):
        self.icici_bank = icici_bank

    def validate_card(self, card: Card) -> bool:
        """Validate card using ICICI bank's proprietary API"""
        return self.icici_bank.validateCard(card.get_card_number())

    def validate_pin(self, card: Card, pin: str) -> bool:
        """Validate PIN using ICICI bank's proprietary API"""
        return self.icici_bank.validatePin(card.get_card_number(), pin)

    def get_account_balance(self, account_number: str) -> float:
        """Get account balance using ICICI bank's proprietary API"""
        return self.icici_bank.balance(account_number)

    def withdraw(self, account_number: str, amount: float) -> None:
        """Withdraw money using ICICI bank's proprietary API"""
        if not self.icici_bank.deduct(account_number, amount):
            raise InsufficientFundsException("Insufficient funds in ICICI account")

    def deposit(self, account_number: str, amount: float) -> None:
        """Deposit money using ICICI bank's proprietary API"""
        if not self.icici_bank.add(account_number, amount):
            raise ValueError(f"Failed to deposit to ICICI account {account_number}")
