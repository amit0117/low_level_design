from app.models.balance_sheet import BalanceSheet
from app.models.transaction import Transaction
from app.observers.base_observer import Observer
from app.models.enums import TransactionStatus
from app.models.expense import Expense
from uuid import uuid4
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from app.models.group import Group


class User(Observer):
    def __init__(self, name: str, email: str):
        super().__init__()
        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.balance_sheet = BalanceSheet(self)
        self.groups: list["Group"] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_balance_sheet(self) -> "BalanceSheet":
        return self.balance_sheet

    def update(self, data: Optional[Any], message: Optional[str]) -> None:
        """Base update method from Observer interface"""
        # This method is required by the Observer interface
        # The specific update methods (transaction_update, update_group, expense_update)
        # are called directly by their respective subjects
        pass

    def transaction_update(self, transaction: Transaction):
        if transaction.get_status() == TransactionStatus.COMPLETED:
            print(
                f"{transaction.get_to_user().get_name()} has paid {transaction.get_from_user().get_name()} an amount of {transaction.get_amount()} amount"
            )
        elif transaction.get_status() == TransactionStatus.FAILED:
            print(
                f"Transaction {transaction.get_id()} between {transaction.get_from_user().get_name()} and {transaction.get_to_user().get_name()} has failed"
            )
        else:
            print(
                f"Transaction {transaction.get_id()} between {transaction.get_from_user().get_name()} and {transaction.get_to_user().get_name()} is pending"
            )

    def update_group(self, message: str):
        print(f"Notification for {self.name}: {message}\n\n")

    def expense_update(self, expense: Expense, message: str):
        print(f"💰 Expense Notification for {self.name}: {message}")
        print(f"   📝 Description: {expense.get_description()}")
        print(f"   💵 Amount: ₹{expense.get_amount():.2f}")
        print(f"   👤 Paid by: {expense.get_paid_by().get_name()}")
        print(f"   👥 Participants: {', '.join([p.get_name() for p in expense.get_participants()])}")
        print()

    def add_group(self, group: "Group"):
        self.groups.append(group)

    def remove_group(self, group: "Group"):
        self.groups.remove(group)

    def print_group_details(self) -> list["Group"]:
        # print all group name for current user
        print(f"Groups for {self.name} till now are as follows:")
        for group in self.groups:
            print(group.get_name())
        print()
