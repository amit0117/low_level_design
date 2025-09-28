from app.models.group import Group
from app.models.user import User
from typing import Optional
from app.models.transaction import Transaction
from app.models.expense import Expense


class GroupService:
    def __init__(self):
        self.groups: dict[str, Group] = {}

    def create_group(self, name: str, members: list[User]) -> Group:
        group = Group(name, members)
        self.groups[group.get_id()] = group
        return group

    def get_group(self, id: str) -> Optional[Group]:
        return self.groups.get(id)

    def get_all_groups(self) -> list[Group]:
        return list(self.groups.values())

    def simplify_group_debts(self, group_id: str) -> list[Transaction]:
        if group_id not in self.groups:
            raise ValueError(f"Group with id {group_id} not found")
        group = self.groups[group_id]
        return group.simplify_expenses()

    def add_expense(self, group_id: str, expense: Expense) -> None:
        if group_id not in self.groups:
            raise ValueError(f"Group with id {group_id} not found")
        group = self.groups[group_id]
        group.add_expense(expense)
