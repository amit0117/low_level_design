from abc import ABC, abstractmethod
from app.models.split import Split
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class SplitStrategy(ABC):
    @abstractmethod
    def calculate_splits(self, total_amount: float, paid_by: "User", participants: list["User"], split_values: Optional[list[float]]) -> list[Split]:
        raise NotImplementedError("Subclasses must implement this method")


class EqualSplitStrategy(SplitStrategy):
    def calculate_splits(self, total_amount: float, paid_by: "User", participants: list["User"], split_values: Optional[list[float]]) -> list[Split]:
        # Exclude the paid_by from the participants because they don't need to pay anything to themselves
        return [Split(participant, total_amount / len(participants)) for participant in participants if participant != paid_by]


class PercentSplitStrategy(SplitStrategy):
    # Validate that the sum of the split_values is 100 and the length of the split_values is the same as the length of the participants

    def calculate_splits(self, total_amount: float, paid_by: "User", participants: list["User"], split_values: Optional[list[float]]) -> list[Split]:
        if not self.validate_split_values(split_values, participants):
            raise ValueError("Invalid split values")
        return [
            Split(participant, total_amount * split_value / 100)
            for participant, split_value in zip(participants, split_values)
            if participant != paid_by
        ]

    def validate_split_values(self, split_values: list[float], participants: list["User"]) -> bool:
        return len(split_values) == len(participants) and abs(sum(split_values) - 100) < 0.01


class ExactSplitStrategy(SplitStrategy):
    def calculate_splits(self, total_amount: float, paid_by: "User", participants: list["User"], split_values: Optional[list[float]]) -> list[Split]:
        if not self.validate_split_values(split_values, participants, total_amount):
            raise ValueError("Invalid split values")
        return [Split(participant, split_value) for participant, split_value in zip(participants, split_values) if participant != paid_by]

    def validate_split_values(self, split_values: list[float], participants: list["User"], total_amount: float) -> bool:
        return len(split_values) == len(participants) and abs(sum(split_values) - total_amount) < 0.01
