from enum import Enum


class TableStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class OrderItemStatus(Enum):
    ORDERED = "ordered"
    PREPARING = "preparing"
    READY_FOR_PICKUP = "ready-for-pickup"
    SERVED = "served"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class MenuCategory(Enum):
    VEG = "veg"
    NON_VEG = "non-veg"


class PaymentMethod(Enum):
    CREDIT_CARD = "credit-card"
    DEBIT_CARD = "debit-card"
    UPI = "upi"
    CASH = "cash"


class StaffRole(Enum):
    WAITER = "waiter"
    CHEF = "chef"
    MANAGER = "manager"
    CLEANER = "cleaner"
    SECURITY = "security"
    OTHER = "other"
