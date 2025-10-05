from app.models.borrow import Borrow
from threading import Lock
from typing import Optional
from app.models.enums import BorrowStatus
from app.models.member import Member
from app.models.library_item import LibraryItem
from datetime import datetime


class BorrowRepository:
    _lock = Lock()
    _instance: "BorrowRepository" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "borrows"):
            return
        self.process_lock = Lock()
        self.borrows: list[Borrow] = []

    @classmethod
    def get_instance(cls) -> "BorrowRepository":
        return cls._instance or cls()

    def add_borrow(self, borrow: Borrow):
        with self.process_lock:
            self.borrows.append(borrow)

    def remove_borrow(self, borrow: Borrow):
        with self.process_lock:
            if not self.get_borrow_by_id(borrow.get_id()):
                raise ValueError("Borrow not found")
            self.borrows.remove(borrow)

    def get_borrow_by_id(self, id: str) -> Optional[Borrow]:
        return next((borrow for borrow in self.borrows if borrow.get_id() == id), None)

    def get_all_borrows(self) -> list[Borrow]:
        return self.borrows

    def get_borrows_by_item(self, item: LibraryItem) -> list[Borrow]:
        return [borrow for borrow in self.borrows if borrow.get_item() == item]

    def get_borrows_by_member(self, member: Member) -> list[Borrow]:
        return [borrow for borrow in self.borrows if borrow.get_borrowed_by() == member]

    def get_borrows_by_status(self, status: BorrowStatus) -> list[Borrow]:
        return [borrow for borrow in self.borrows if borrow.get_status() == status]

    def get_borrows_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Borrow]:
        return [borrow for borrow in self.borrows if borrow.get_borrow_date() >= start_date and borrow.get_borrow_date() <= end_date]
