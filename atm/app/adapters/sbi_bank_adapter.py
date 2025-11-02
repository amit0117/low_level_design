from app.models.bank_server import BankServer
from app.models.banks.sbi_bank import SBIBank
from app.models.card import Card
from app.exceptions.insufficient_money import InsufficientFundsException


class SBIBankAdapter(BankServer):
    """
    Adapter for SBI Bank
    Translates BankServer interface to SBI proprietary API
    """

    def __init__(self, sbi_bank: SBIBank):
        self.sbi_bank = sbi_bank

    def validate_card(self, card: Card) -> bool:
        """Validate card using SBI bank's proprietary API"""
        return self.sbi_bank.validateCard(card.get_card_number())

    def validate_pin(self, card: Card, pin: str) -> bool:
        """Validate PIN using SBI bank's proprietary API"""
        return self.sbi_bank.validatePin(card.get_card_number(), pin)

    def get_account_balance(self, account_number: str) -> float:
        """Get account balance using SBI bank's proprietary API"""
        return self.sbi_bank.getBalance(account_number)

    def withdraw(self, account_number: str, amount: float) -> None:
        """Withdraw money using SBI bank's proprietary API"""
        if not self.sbi_bank.transferOut(account_number, amount):
            raise InsufficientFundsException("Insufficient funds in SBI account")

    def deposit(self, account_number: str, amount: float) -> None:
        """Deposit money using SBI bank's proprietary API"""
        if not self.sbi_bank.transferIn(account_number, amount):
            raise ValueError(f"Failed to deposit to SBI account {account_number}")
