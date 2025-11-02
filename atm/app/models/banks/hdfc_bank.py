from threading import Lock
from app.models.account import Account
from typing import Dict, Optional


class HDFCBank:
    """
    Mock HDFC Bank with proprietary API interface
    Uses methods: checkBalance(), debitAmount(), creditAmount()
    """

    def __init__(self):
        self.accounts: Dict[str, Account] = {}  # account_number -> Account
        self.cards: Dict[str, str] = {}  # card_number -> account_number mapping
        self.pins: Dict[str, str] = {}  # card_number -> pin mapping
        self.lock = Lock()

    def checkBalance(self, account_num: str) -> float:
        """Check account balance - HDFC proprietary method"""
        with self.lock:
            account = self.accounts.get(account_num)
            if account:
                return account.get_balance()
            return 0.0

    def debitAmount(self, account_num: str, amt: float) -> bool:
        """Debit amount from account - HDFC proprietary method. Returns True if successful, False otherwise"""
        with self.lock:
            account = self.accounts.get(account_num)
            if not account:
                return False
            try:
                account.withdraw(amt)
                return True
            except Exception:
                return False

    def creditAmount(self, account_num: str, amt: float) -> bool:
        """Credit amount to account - HDFC proprietary method. Returns True if successful, False otherwise"""
        with self.lock:
            account = self.accounts.get(account_num)
            if not account:
                return False
            try:
                account.deposit(amt)
                return True
            except Exception:
                return False

    def addAccount(self, account: Account) -> None:
        """Add an account to HDFC bank"""
        with self.lock:
            self.accounts[account.get_account_number()] = account

    def addCard(self, card_number: str, account_num: str, pin: str) -> None:
        """Add card mapping for HDFC bank"""
        with self.lock:
            self.cards[card_number] = account_num
            self.pins[card_number] = pin

    def validateCard(self, card_number: str) -> bool:
        """Validate if card exists in HDFC system"""
        with self.lock:
            return card_number in self.cards

    def validatePin(self, card_number: str, pin: str) -> bool:
        """Validate PIN for HDFC card"""
        with self.lock:
            return self.pins.get(card_number) == pin

    def getAccountByCard(self, card_number: str) -> Optional[str]:
        """Get account number by card number"""
        with self.lock:
            return self.cards.get(card_number)
