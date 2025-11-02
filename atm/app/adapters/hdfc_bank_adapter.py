from app.models.bank_server import BankServer
from app.models.banks.hdfc_bank import HDFCBank
from app.models.card import Card
from app.exceptions.insufficient_money import InsufficientFundsException


class HDFCBankAdapter(BankServer):
    """
    Adapter for HDFC Bank
    Translates BankServer interface to HDFC proprietary API
    """

    def __init__(self, hdfc_bank: HDFCBank):
        self.hdfc_bank = hdfc_bank

    def validate_card(self, card: Card) -> bool:
        """Validate card using HDFC bank's proprietary API"""
        return self.hdfc_bank.validateCard(card.get_card_number())

    def validate_pin(self, card: Card, pin: str) -> bool:
        """Validate PIN using HDFC bank's proprietary API"""
        return self.hdfc_bank.validatePin(card.get_card_number(), pin)

    def get_account_balance(self, account_number: str) -> float:
        """Get account balance using HDFC bank's proprietary API"""
        return self.hdfc_bank.checkBalance(account_number)

    def withdraw(self, account_number: str, amount: float) -> None:
        """Withdraw money using HDFC bank's proprietary API"""
        if not self.hdfc_bank.debitAmount(account_number, amount):
            raise InsufficientFundsException("Insufficient funds in HDFC account")

    def deposit(self, account_number: str, amount: float) -> None:
        """Deposit money using HDFC bank's proprietary API"""
        if not self.hdfc_bank.creditAmount(account_number, amount):
            raise ValueError(f"Failed to deposit to HDFC account {account_number}")
