from threading import Lock
from typing import Dict, Optional
from app.models.account import Account


class ICICIBank:
    """
    Mock ICICI Bank with proprietary API interface
    Uses methods: balance(), deduct(), add()
    """

    def __init__(self):
        self.accounts: Dict[str, Account] = {}  # account_number -> Account
        self.cards: Dict[str, str] = {}  # card_number -> account_number mapping
        self.pins: Dict[str, str] = {}  # card_number -> pin mapping
        self.lock = Lock()

    def balance(self, account_num: str) -> float:
        """Get account balance - ICICI proprietary method"""
        with self.lock:
            account = self.accounts.get(account_num)
            if account:
                return account.get_balance()
            return 0.0

    def deduct(self, account_num: str, amt: float) -> bool:
        """Deduct amount from account - ICICI proprietary method. Returns True if successful, False otherwise"""
        with self.lock:
            account = self.accounts.get(account_num)
            if not account:
                return False
            try:
                account.withdraw(amt)
                return True
            except Exception:
                return False

    def add(self, account_num: str, amt: float) -> bool:
        """Add amount to account - ICICI proprietary method. Returns True if successful, False otherwise"""
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
        """Add an account to ICICI bank"""
        with self.lock:
            self.accounts[account.get_account_number()] = account

    def addCard(self, card_number: str, account_num: str, pin: str) -> None:
        """Add card mapping for ICICI bank"""
        with self.lock:
            self.cards[card_number] = account_num
            self.pins[card_number] = pin

    def validateCard(self, card_number: str) -> bool:
        """Validate if card exists in ICICI system"""
        with self.lock:
            return card_number in self.cards

    def validatePin(self, card_number: str, pin: str) -> bool:
        """Validate PIN for ICICI card"""
        with self.lock:
            return self.pins.get(card_number) == pin

    def getAccountByCard(self, card_number: str) -> Optional[str]:
        """Get account number by card number"""
        with self.lock:
            return self.cards.get(card_number)
