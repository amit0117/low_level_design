from app.observers.base_observer import Subject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.expense import Expense


class ExpenseSubject(Subject):
    """Subject for expense-related notifications"""

    def notify_observers(self, data: "Expense", message: str) -> None:
        for observer in self._observers:
            observer.expense_update(data, message)
