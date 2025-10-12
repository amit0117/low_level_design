from app.models.account import Account
from threading import Lock
from typing import Optional


class AccountRepository:
    _instance: Optional["AccountRepository"] = None
    _lock = Lock()

    def __new__(cls) -> "AccountRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "accounts"):
            return
        # Account_number -> Account
        self.accounts: dict[str, Account] = {}

    @classmethod
    def get_instance(cls) -> "AccountRepository":
        return cls._instance or cls()

    def add_account(self, account: Account) -> None:
        self.accounts[account.get_account_number()] = account

    def get_account(self, account_number: str) -> Optional[Account]:
        return self.accounts.get(account_number)

    def get_account_by_vpa(self, vpa: str) -> Optional[Account]:
        return next((account for account in self.accounts.values() if account.get_vpa() == vpa), None)

    def update_account(self, account: Account) -> None:
        self.accounts[account.get_account_number()] = account

    def delete_account(self, account_number: str) -> None:
        self.accounts.pop(account_number, None)

    def get_all_accounts(self) -> list[Account]:
        return list(self.accounts.values())

    def get_all_account_for_a_user(self, user_id: str) -> list[Account]:
        return [account for account in self.accounts.values() if account.get_user().get_id() == user_id]

    def get_all_accounts_for_a_bank(self, bank_name: str) -> list[Account]:
        return [account for account in self.accounts.values() if account.get_bank_name() == bank_name]
