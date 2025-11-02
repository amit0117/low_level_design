from datetime import datetime, timedelta
from typing import Dict, Optional
from threading import Lock
from app.models.atm import ATM
from app.models.user import User, Customer, Admin
from app.models.account import Account
from app.models.card import Card
from app.models.card_reader import CardReader
from app.models.keypad import Keypad
from app.models.cash_dispenser import CashDispenser
from app.models.enums import AccountType, UserType
from app.models.banks.hdfc_bank import HDFCBank
from app.models.banks.sbi_bank import SBIBank
from app.models.banks.icici_bank import ICICIBank
from app.adapters.hdfc_bank_adapter import HDFCBankAdapter
from app.adapters.sbi_bank_adapter import SBIBankAdapter
from app.adapters.icici_bank_adapter import ICICIBankAdapter
from app.repositories.bank_repository import BankRepository
from app.services.transaction_service import TransactionService


class ATMMachine:
    _instance: Optional["ATMMachine"] = None
    _lock: Lock = Lock()
    _initialized: bool = False

    def __new__(cls, atm_name: str = "Main ATM", initial_cash: float = 100000.0) -> "ATMMachine":
        """Singleton implementation with thread safety"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._atm_name = atm_name
                    cls._instance._initial_cash = initial_cash
        return cls._instance

    def __init__(self, atm_name: str = "Main ATM", initial_cash: float = 100000.0):
        """Initialize the ATM machine (only once due to singleton)"""
        if self._initialized:
            return

        atm_name = getattr(self, "_atm_name", atm_name)
        initial_cash = getattr(self, "_initial_cash", initial_cash)
        print(f"\n{'='*60}")
        print(f"🚀 Initializing ATM Machine: {atm_name}")
        print(f"{'='*60}\n")

        # Initialize banks
        self.hdfc_bank = HDFCBank()
        self.sbi_bank = SBIBank()
        self.icici_bank = ICICIBank()

        # Create adapters
        self.hdfc_adapter = HDFCBankAdapter(self.hdfc_bank)
        self.sbi_adapter = SBIBankAdapter(self.sbi_bank)
        self.icici_adapter = ICICIBankAdapter(self.icici_bank)

        # Register banks in repository
        self.bank_repository = BankRepository.get_instance()
        self.bank_repository.add_bank_server("HDFC", self.hdfc_adapter)
        self.bank_repository.add_bank_server("SBI", self.sbi_adapter)
        self.bank_repository.add_bank_server("ICICI", self.icici_adapter)

        print("✅ Banks registered: HDFC, SBI, ICICI")

        # Initialize ATM components
        self.card_reader = CardReader()
        self.keypad = Keypad()
        self.cash_dispenser = CashDispenser(initial_cash=initial_cash, low_cash_threshold=5000.0)

        # Create ATM (using HDFC as default bank server - ATM can switch dynamically)
        self.atm = ATM(
            name=atm_name, bank_server=self.hdfc_adapter, card_reader=self.card_reader, keypad=self.keypad, cash_dispenser=self.cash_dispenser
        )

        # Transaction service
        self.transaction_service = TransactionService(self.atm)

        # Store users, accounts, and cards for easy access
        self.users: Dict[str, User] = {}
        self.accounts: Dict[str, Account] = {}
        self.cards: Dict[str, Card] = {}
        self.card_to_account: Dict[str, Account] = {}
        self.card_to_user: Dict[str, User] = {}
        self.account_pins: Dict[str, str] = {}  # account_number -> pin

        print(f"✅ ATM Machine initialized successfully!")
        print(f"   ATM ID: {self.atm.get_id()[:8]}")
        print(f"   Initial Cash: ₹{initial_cash:,.2f}")
        print(f"   Banks Available: {self.bank_repository.get_all_banks()}\n")

        self._initialized = True

    @classmethod
    def get_instance(cls, atm_name: str = "Main ATM", initial_cash: float = 100000.0) -> "ATMMachine":
        """Get the singleton instance of ATMMachine"""
        return cls(atm_name=atm_name, initial_cash=initial_cash)

    def add_user(
        self, name: str, bank_name: str, account_number: str, account_type: AccountType, initial_balance: float, pin: str, card_number: str
    ) -> User:
        # Create account first with None user
        account = Account(account_number=account_number, account_type=account_type, balance=initial_balance, user=None, bank_name=bank_name)

        # Create user with account (Customer.__init__ calls super().__init__(name, account, UserType.CUSTOMER)
        # But User.__init__ expects (name, user_type, accounts, cards), so account is incorrectly passed as user_type
        # We'll fix this after creation
        user = Customer(name=name, account=account)

        # Fix the user object - reinitialize properly
        # Clear incorrect state and set up properly
        user.accounts = [account]
        user.user_type = UserType.CUSTOMER
        account.user = user

        # Create card
        expiration_date = datetime.now() + timedelta(days=5 * 365)  # 5 years validity
        card = Card(card_number=card_number, cvv="123", expiration_date=expiration_date)

        # Link card to user
        user.add_card(card)

        # Get bank instance and add account/card
        bank = self._get_bank_instance(bank_name)
        bank.addAccount(account)
        bank.addCard(card_number, account_number, pin)

        # Store in dictionaries
        self.users[name] = user
        self.accounts[account_number] = account
        self.cards[card_number] = card
        self.card_to_account[card_number] = account
        self.card_to_user[card_number] = user
        self.account_pins[account_number] = pin

        print(f"✅ User added: {name}")
        print(f"   Account: {account_number} ({bank_name})")
        print(f"   Card: {card_number}")
        print(f"   Balance: ₹{initial_balance:,.2f}\n")

        return user

    def add_admin(self, name: str, bank_name: str, account_number: str, account_type: AccountType, initial_balance: float) -> Admin:
        # Create admin account first with None user (will be set later)
        # Admin.__init__ has: super().__init__(name, account, UserType.ADMIN)
        # But User.__init__ expects: (name, user_type, accounts=None, cards=None)
        # So Admin constructor passes account as user_type which is wrong
        # We'll create account without user first, then link them
        account = Account(
            account_number=account_number,
            account_type=account_type,
            balance=initial_balance,
            user=None,  # Will be set after admin creation
            bank_name=bank_name,
        )

        # Create admin - this will call super().__init__(name, account, UserType.ADMIN)
        # But User expects (name, user_type, accounts, cards)
        # So we need to fix this after creation
        admin = Admin(name=name, account=account)

        # Fix the admin object - reinitialize properly
        # Clear incorrect state and set up properly
        admin.accounts = [account]
        admin.user_type = UserType.ADMIN
        account.user = admin

        # Get bank and add account
        bank = self._get_bank_instance(bank_name)
        bank.addAccount(account)

        # Add admin as observer for cash dispenser
        self.cash_dispenser.add_admin_observer(admin)

        self.users[name] = admin
        self.accounts[account_number] = account

        print(f"✅ Admin added: {name}")
        print(f"   Account: {account_number} ({bank_name})")
        print(f"   Balance: ₹{initial_balance:,.2f}\n")

        return admin

    def _get_bank_instance(self, bank_name: str):
        if bank_name.upper() == "HDFC":
            return self.hdfc_bank
        elif bank_name.upper() == "SBI":
            return self.sbi_bank
        elif bank_name.upper() == "ICICI":
            return self.icici_bank
        else:
            raise ValueError(f"Unknown bank: {bank_name}")

    def authenticate_user(self, card_number: str, pin: str) -> Optional[tuple[Account, Card]]:
        if card_number not in self.cards:
            print("❌ Invalid card number")
            return None

        card = self.cards[card_number]
        account = self.card_to_account[card_number]
        bank_name = account.get_bank_name()

        # Validate card and PIN using bank server
        bank_server = self.bank_repository.get_bank_server(bank_name)

        if not bank_server.validate_card(card):
            print("❌ Invalid card")
            return None

        if not bank_server.validate_pin(card, pin):
            print("❌ Invalid PIN")
            return None

        print(f"✅ Authentication successful for card: {card_number}")
        return (account, card)

    def balance_inquiry(self, card_number: str, pin: str) -> Optional[float]:
        auth_result = self.authenticate_user(card_number, pin)
        if not auth_result:
            return None

        account, card = auth_result
        try:
            balance = self.transaction_service.balance_inquiry(account, card, pin)
            return balance
        except Exception as e:
            print(f"❌ Balance inquiry failed: {e}")
            return None

    def withdraw(self, card_number: str, pin: str, amount: float) -> bool:
        auth_result = self.authenticate_user(card_number, pin)
        if not auth_result:
            return False

        account, card = auth_result
        try:
            return self.transaction_service.debit(account, card, pin, amount)
        except Exception as e:
            print(f"❌ Withdrawal failed: {e}")
            return False

    def deposit(self, card_number: str, pin: str, amount: float) -> bool:
        auth_result = self.authenticate_user(card_number, pin)
        if not auth_result:
            return False

        account, card = auth_result
        try:
            return self.transaction_service.credit(account, card, pin, amount)
        except Exception as e:
            print(f"❌ Deposit failed: {e}")
            return False

    def transfer(self, source_card_number: str, pin: str, destination_account_number: str, amount: float) -> bool:
        auth_result = self.authenticate_user(source_card_number, pin)
        if not auth_result:
            return False

        source_account, card = auth_result

        if destination_account_number not in self.accounts:
            print(f"❌ Destination account not found: {destination_account_number}")
            return False

        destination_account = self.accounts[destination_account_number]

        try:
            return self.transaction_service.transfer(source_account, destination_account, card, pin, amount)
        except Exception as e:
            print(f"❌ Transfer failed: {e}")
            return False

    def get_account_info(self, card_number: str) -> Optional[dict]:
        if card_number not in self.card_to_account:
            return None

        account = self.card_to_account[card_number]
        return self.transaction_service.get_account_info(account)

    def get_atm_status(self) -> dict:
        return self.transaction_service.get_atm_status()

    def add_cash_to_atm(self, admin_name: str, amount: float) -> None:
        if admin_name not in self.users:
            print(f"❌ Admin not found: {admin_name}")
            return

        admin = self.users[admin_name]
        if not isinstance(admin, Admin):
            print(f"❌ User is not an admin: {admin_name}")
            return

        self.cash_dispenser.add_cash(amount, admin)
        print(f"✅ Cash added: ₹{amount:,.2f}")
        print(f"   Total cash available: ₹{self.cash_dispenser.get_cash_available():,.2f}\n")

    def display_all_users(self) -> None:
        print(f"\n{'='*60}")
        print("👥 Registered Users")
        print(f"{'='*60}")
        for name, user in self.users.items():
            print(f"\n📌 {name} ({user.get_user_type().value})")
            for account in user.get_accounts():
                bank_server = self.bank_repository.get_bank_server(account.get_bank_name())
                balance = bank_server.get_account_balance(account.get_account_number())
                print(f"   Account: {account.get_account_number()} ({account.get_bank_name()})")
                print(f"   Type: {account.get_account_type().value}")
                print(f"   Balance: ₹{balance:,.2f}")
            for card in user.get_cards():
                print(f"   Card: {card.get_card_number()}")
        print(f"\n{'='*60}\n")

    def display_atm_info(self) -> None:
        status = self.get_atm_status()
        print(f"\n{'='*60}")
        print("🏧 ATM Information")
        print(f"{'='*60}")
        print(f"ATM Name: {status['atm_name']}")
        print(f"ATM ID: {status['atm_id'][:8]}")
        print(f"Status: {status['status']}")
        print(f"Cash Available: ₹{status['cash_available']:,.2f}")
        print(f"Low Cash Threshold: ₹{status['low_cash_threshold']:,.2f}")
        print(f"Banks: {', '.join(self.bank_repository.get_all_banks())}")
        print(f"{'='*60}\n")

    def list_available_transactions(self) -> None:
        self.atm.list_available_transactions_options()
