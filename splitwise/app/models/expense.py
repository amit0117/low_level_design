from datetime import datetime
from app.strategies.split_strategy import SplitStrategy
from app.models.split import Split
from app.observers.expense_observer import ExpenseSubject
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Expense(ExpenseSubject):
    def __init__(
        self,
        id: str,
        description: str,
        amount: float,
        paid_by: "User",
        participants: list["User"],
        split_strategy: SplitStrategy,
        split_values: Optional[list[float]],
    ):
        super().__init__()
        self.id = id
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.participants = participants
        self.split_strategy = split_strategy
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.split_values = split_values

        # Add all participants as observers (including the person who paid)
        for participant in participants:
            self.add_observer(participant)

    def get_description(self) -> str:
        return self.description

    def get_amount(self) -> float:
        return self.amount

    def get_paid_by(self) -> "User":
        return self.paid_by

    def get_participants(self) -> list["User"]:
        return self.participants

    def get_splits(self) -> list[Split]:
        return self.split_strategy.calculate_splits(self.amount, self.paid_by, self.participants, self.split_values)

    def get_split_strategy(self) -> SplitStrategy:
        return self.split_strategy

    def get_created_at(self) -> str:
        return self.created_at

    def get_id(self) -> str:
        return self.id
