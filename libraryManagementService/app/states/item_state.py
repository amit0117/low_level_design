from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from app.models.enums import ItemStatus

if TYPE_CHECKING:
    from app.models.library_item import LibraryItem


class ItemState(ABC):
    @abstractmethod
    def reserve(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def release(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def issue(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def return_item(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def mark_lost(self, item: "LibraryItem"):
        raise NotImplementedError("Subclasses must implement this method")


class AvailableState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print(f"Item {item.id} is reserved now")
        item.set_state(ReservedState())
        item.set_status(ItemStatus.RESERVED)

    def release(self, item: "LibraryItem"):
        print("This item is already available, so can't release it")

    def issue(self, item: "LibraryItem"):
        print("Can't issue an available item, first reserve it")

    def return_item(self, item: "LibraryItem"):
        print("This item is not issued, so can't return it")

    def mark_lost(self, item: "LibraryItem"):
        print(f"Item {item.id} is marked as lost")
        item.set_state(LostState())
        item.set_status(ItemStatus.MISSING)


class ReservedState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print(f"Item {item.id} is already reserved")

    def release(self, item: "LibraryItem"):
        print(f"Item {item.id} is released now and is available to book")
        item.set_state(AvailableState())
        item.set_status(ItemStatus.AVAILABLE)

    def issue(self, item: "LibraryItem"):
        print(f"Item {item.id} is issued now")
        item.set_state(IssuedState())
        item.set_status(ItemStatus.ISSUED)

    def return_item(self, item: "LibraryItem"):
        print("This item is not issued, so can't return it")

    def mark_lost(self, item: "LibraryItem"):
        print("Item is already reserved, so can't mark it as lost")


class IssuedState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print("This item is already issued, so can't reserve it")

    def release(self, item: "LibraryItem"):
        print("This item is already issued, so can't release it")

    def issue(self, item: "LibraryItem"):
        print("This item is already issued, so can't issue it")

    def return_item(self, item: "LibraryItem"):
        print(f"Item {item.id} is returned now and is available to book")
        item.set_state(AvailableState())
        item.set_status(ItemStatus.AVAILABLE)

    def mark_lost(self, item: "LibraryItem"):
        print(f"Item {item.id} is marked as lost")
        item.set_state(LostState())
        item.set_status(ItemStatus.MISSING)


class LostState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print("This item is already lost, so can't reserve it")

    def release(self, item: "LibraryItem"):
        print("This item is already lost, so can't release it")

    def issue(self, item: "LibraryItem"):
        print("This item is already lost, so can't issue it")

    def return_item(self, item: "LibraryItem"):
        print("This item is already lost, so can't return it")

    def mark_lost(self, item: "LibraryItem"):
        print("This item is already lost, so can't mark it as lost")


class DamagedState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print("This item is already damaged, so can't reserve it")

    def release(self, item: "LibraryItem"):
        print("This item is already damaged, so can't release it")

    def issue(self, item: "LibraryItem"):
        print("This item is already damaged, so can't issue it")

    def return_item(self, item: "LibraryItem"):
        print("This item is already damaged, so can't return it")

    def mark_lost(self, item: "LibraryItem"):
        print("This item is already damaged, so can't mark it as lost")


class WithdrawnState(ItemState):
    def reserve(self, item: "LibraryItem"):
        print("This item is already withdrawn, so can't reserve it")

    def release(self, item: "LibraryItem"):
        print("This item is already withdrawn, so can't release it")

    def issue(self, item: "LibraryItem"):
        print("This item is already withdrawn, so can't issue it")

    def return_item(self, item: "LibraryItem"):
        print("This item is already withdrawn, so can't return it")

    def mark_lost(self, item: "LibraryItem"):
        print("This item is already withdrawn, so can't mark it as lost")
