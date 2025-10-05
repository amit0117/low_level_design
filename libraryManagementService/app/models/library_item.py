from app.models.enums import ItemType, ItemStatus
from uuid import uuid4
from typing import Optional, TYPE_CHECKING
from app.observers.item_observer import ItemSubject
from app.states.item_state import ItemState, AvailableState, DamagedState

if TYPE_CHECKING:
    from app.models.member import Member


class LibraryItem(ItemSubject):
    def __init__(self, title: str, author: str, type: ItemType, status: Optional[ItemStatus] = None):
        super().__init__()
        self.id = str(uuid4())
        self.title = title
        self.author = author
        self.type = type
        self.status = status or ItemStatus.AVAILABLE
        self.state: ItemState = AvailableState()

    def get_id(self) -> str:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_author(self) -> str:
        return self.author

    def get_type(self) -> ItemType:
        return self.type

    def get_status(self) -> ItemStatus:
        return self.status

    def set_status(self, status: ItemStatus):
        self.status = status
        self.notify_observers(self)

    def set_state(self, state: ItemState):
        self.state = state

    def get_state(self) -> ItemState:
        return self.state

    def reserve(self, member: "Member"):
        # add member to observers
        self.observers.append(member)
        self.state.reserve(self)

    def release(self, member: "Member"):
        # remove member from observers
        self.observers.remove(member)
        self.state.release(self)

    def issue(self):
        self.state.issue(self)

    def return_item(self, member: "Member"):
        # remove member from observers
        self.observers.remove(member)
        self.state.return_item(self)

    def mark_lost(self):
        self.state.mark_lost(self)

    def mark_damaged(self):
        self.set_status(ItemStatus.DAMAGED)
        self.set_state(DamagedState())

    def mark_overdue(self):
        self.set_status(ItemStatus.OVERDUE)

    def display_info(self):
        print(f"Item: {self.title} (ID: {self.id})")
        print(f"Author: {self.author}")
        print(f"Type: {self.type.value}")
        print(f"Status: {self.status.value}")
