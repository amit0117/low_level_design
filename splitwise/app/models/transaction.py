from typing import TYPE_CHECKING
from uuid import uuid4
from app.models.enums import TransactionStatus
from app.observers.transaction_observer import TransactionSubject

if TYPE_CHECKING:
    from app.models.user import User


# Transaction class represents a transaction between a user and a group
class Transaction(TransactionSubject):
    def __init__(self, from_user: "User", to_user: "User", amount: float):
        super().__init__()
        self.id = str(uuid4())
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount
        self.status = TransactionStatus.PENDING
        # Add the observers for the transaction
        self.add_observer(from_user)
        self.add_observer(to_user)

    def get_id(self):
        return self.id

    def get_from_user(self):
        return self.from_user

    def get_to_user(self):
        return self.to_user

    def get_amount(self):
        return self.amount

    def get_status(self):
        return self.status

    def set_status(self, status: TransactionStatus):
        self.status = status
        self.notify_observers(data=self)

    def __str__(self):
        return f"{self.from_user.get_name()} should pay {self.to_user.get_name()} {self.amount:.2f}"
