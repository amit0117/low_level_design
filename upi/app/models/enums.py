from enum import Enum


class Currency(Enum):
    INR = "INR"
    USD = "USD"
    JPY = "JPY"


class TransactionStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


class PaymentType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class CommandStatus(Enum):
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(Enum):
    UPI_PUSH = "UPI_PUSH"
    UPI_PULL = "UPI_PULL"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    NET_BANKING = "NET_BANKING"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    WALLET = "WALLET"


class AccountType(Enum):
    SAVINGS = "SAVINGS"
    FIXED_DEPOSIT = "FIXED_DEPOSIT"
    LOAN = "LOAN"
