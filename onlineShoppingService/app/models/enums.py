from enum import Enum


class OrderStatus(Enum):
    PENDING = "PENDING"
    PLACED = "PLACED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentMethod(Enum):
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    UPI = "UPI"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"


class UserType(Enum):
    ADMIN = "ADMIN"
    NORMAL_USER = "NORMAL_USER"


class ProductCategory(Enum):
    ELECTRONICS = "ELECTRONICS"
    GROCERY = "GROCERY"
    CLOTHING = "CLOTHING"
    BOOKS = "BOOKS"
    OTHER = "OTHER"


class ProductStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
