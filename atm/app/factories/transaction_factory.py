from abc import ABC, abstractmethod
from app.models.transactions.transaction import Transaction
from app.models.transactions.withdrawal_transaction import WithdrawalTransaction
from app.models.transactions.deposit_transaction import DepositTransaction
from app.models.transactions.transfer_transaction import TransferTransaction
from app.models.transactions.balance_inquiry_transaction import BalanceInquiryTransaction
from typing import Any
from app.models.account import Account
from app.models.cash_dispenser import CashDispenser
from app.models.card import Card


class TransactionFactory(ABC):
    @abstractmethod
    def create_transaction(self, *args: Any) -> Transaction:
        raise NotImplementedError("create_transaction method must be implemented")


class WithdrawalTransactionFactory(TransactionFactory):
    def create_transaction(
        self, bank_name: str, account: Account, amount: float, cash_dispenser: CashDispenser, card: Card, pin: str
    ) -> WithdrawalTransaction:
        return WithdrawalTransaction(bank_name, account, amount, cash_dispenser, card, pin)


class DepositTransactionFactory(TransactionFactory):
    def create_transaction(self, bank_name: str, account: Account, amount: float, card: Card, pin: str) -> DepositTransaction:
        return DepositTransaction(bank_name, account, amount, card, pin)


class TransferTransactionFactory(TransactionFactory):
    def create_transaction(
        self,
        source_bank_name: str,
        destination_bank_name: str,
        source_account: Account,
        destination_account: Account,
        amount: float,
        card: Card,
        pin: str,
    ) -> TransferTransaction:
        return TransferTransaction(source_bank_name, destination_bank_name, source_account, destination_account, amount, card, pin)


class BalanceInquiryTransactionFactory(TransactionFactory):
    def create_transaction(self, bank_name: str, account: Account, card: Card, pin: str) -> BalanceInquiryTransaction:
        return BalanceInquiryTransaction(bank_name, account, card, pin)
