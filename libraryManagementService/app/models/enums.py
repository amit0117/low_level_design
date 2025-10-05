from enum import Enum


class ItemType(Enum):
    BOOK = "book"
    MAGAZINE = "magazine"
    NEWSPAPER = "newspaper"
    JOURNAL = "journal"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    REPORT = "report"
    MAPS_AND_ATLAS = "maps_and_atlas"
    OTHER = "other"


class ItemStatus(Enum):
    AVAILABLE = "available"  # item is on the shelf and can be borrowed
    RESERVED = "reserved"  # item is set aside for a member who has requested it
    ISSUED = "issued"  # item is borrowed by a member
    MISSING = "missing"  # reported missing by the borrower or library
    OVERDUE = "overdue"  # borrowed item not returned within the due date
    DAMAGED = "damaged"  # tem is unusable and awaiting repair/replacement
    WITHDRAWN = "withdrawn"  # permanently removed from collection
    REFERENCE_ONLY = "reference_only"  # cannot be borrowed, only used inside the library
    OTHER = "other"


class BorrowStatus(Enum):
    REQUESTED = "requested"  # user requested to borrow the item
    ACTIVE = "active"  # borrow is ongoing
    RETURNED = "returned"  # item has been returned
    OVERDUE = "overdue"  # not returned by due date
    CANCELLED = "cancelled"  # user cancelled the borrow request before borrowing the item


class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
