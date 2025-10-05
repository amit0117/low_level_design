from uuid import uuid4
from typing import TYPE_CHECKING
from app.observers.item_observer import ItemObserver

if TYPE_CHECKING:
    from app.models.borrow import Borrow
    from app.models.library_item import LibraryItem


class Member(ItemObserver):
    def __init__(self, name: str):
        self.id = str(uuid4())
        self.name = name
        self.borrow_history: list["Borrow"] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_borrow_history(self) -> list["Borrow"]:
        return self.borrow_history

    def add_to_borrow_history(self, borrow: "Borrow"):
        self.borrow_history.append(borrow)

    def set_name(self, name: str):
        self.name = name

    def update(self, item: "LibraryItem"):
        """Observer pattern implementation - notify member about item status changes"""
        print(f"Notification to {self.name}: Item '{item.get_title()}' status changed to {item.get_status().value}")

    def __str__(self) -> str:
        return f"Member: {self.name}\n, total bookings: {len(self.borrow_history)}\n"
