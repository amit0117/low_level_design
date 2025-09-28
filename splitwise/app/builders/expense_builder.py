from uuid import uuid4
from app.models.expense import Expense
from app.strategies.split_strategy import SplitStrategy
from app.models.user import User


# Created a builder pattern because this is a complex object and have some optional parameters (like split values)
class ExpenseBuilder:
    def __init__(self):
        self.id = str(uuid4())
        self.description = None
        self.amount = None
        self.paid_by = None
        self.participants = None
        self.split_strategy = None
        self.split_values = None

    def set_id(self, id: str) -> "ExpenseBuilder":
        self.id = id
        return self

    def set_description(self, description: str) -> "ExpenseBuilder":
        self.description = description
        return self

    def set_amount(self, amount: float) -> "ExpenseBuilder":
        self.amount = amount
        return self

    def set_paid_by(self, paid_by: User) -> "ExpenseBuilder":
        self.paid_by = paid_by
        return self

    def set_participants(self, participants: list[User]) -> "ExpenseBuilder":
        self.participants = participants
        return self

    def set_split_strategy(self, split_strategy: SplitStrategy) -> "ExpenseBuilder":
        self.split_strategy = split_strategy
        return self

    def set_split_values(self, split_values: list[float]) -> "ExpenseBuilder":
        self.split_values = split_values
        return self

    def validate_expense(self) -> None:
        if self.split_strategy is None:
            raise ValueError("Split strategy is required")
        if self.split_values is not None and len(self.split_values) != len(self.participants):
            raise ValueError("Split values must be the same length as participants")

    def build(self) -> Expense:
        self.validate_expense()
        return Expense(self.id, self.description, self.amount, self.paid_by, self.participants, self.split_strategy, self.split_values)
