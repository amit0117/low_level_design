from app.models.library_item import LibraryItem
from app.models.enums import BorrowStatus
from typing import TYPE_CHECKING
from datetime import datetime, timedelta
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.member import Member


# 1:1 mapping between library item and user
class Borrow:
    def __init__(self, item: LibraryItem, borrowed_by: "Member", duration_in_days: int):
        self.id = str(uuid4())
        self.item = item
        self.borrowed_by = borrowed_by
        self.borrow_date = None
        self.due_date = None  # Will be set when item is actually borrowed
        self.return_date = None
        self.renewal_count = 0
        self.fine_amount = 0
        self.status = BorrowStatus.REQUESTED
        self.duration_in_days = duration_in_days

    def get_id(self) -> str:
        return self.id

    def get_item(self) -> LibraryItem:
        return self.item

    def get_status(self) -> BorrowStatus:
        return self.status

    def get_borrowed_by(self) -> "Member":
        return self.borrowed_by

    def get_borrow_date(self) -> datetime:
        return self.borrow_date

    def get_due_date(self) -> datetime:
        return self.due_date

    def get_return_date(self) -> datetime:
        return self.return_date

    def get_renewal_count(self) -> int:
        return self.renewal_count

    def get_fine_amount(self) -> float:
        return self.fine_amount

    def set_status(self, status: BorrowStatus):
        self.status = status

    def set_return_date(self, return_date: datetime):
        self.return_date = return_date

    def add_fine_amount(self, fine_amount: float):
        self.fine_amount += fine_amount

    def renew(self, duration_in_days: int):
        if self.status != BorrowStatus.ACTIVE:
            raise ValueError("Cannot renew an item that is not active")
        self.renewal_count += 1
        self.due_date += timedelta(days=duration_in_days)
        self.status = BorrowStatus.ACTIVE

    # No need to implement state pattern for borrow as the transition is fairly simple
    # The transitions are: REQUESTED → ACTIVE → RETURNED / OVERDUE / CANCELLED
    def borrow(self):
        if self.status != BorrowStatus.REQUESTED:
            raise ValueError("Cannot borrow an item that is not requested")
        self.status = BorrowStatus.ACTIVE
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=self.duration_in_days)
        self.item.issue()

    def cancel(self):
        if self.status != BorrowStatus.REQUESTED:
            raise ValueError("Cannot cancel a borrow that is not requested")
        self.status = BorrowStatus.CANCELLED
        self.item.release(self.borrowed_by)

    def return_item(self):
        if self.status != BorrowStatus.ACTIVE:
            raise ValueError("Cannot return an item that is not active")
        self.status = BorrowStatus.RETURNED
        self.set_return_date(datetime.now())
        self.item.return_item(self.borrowed_by)
