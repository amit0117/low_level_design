from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
from app.repositories.account_repository import AccountRepository


@dataclass
class StandardizedResponse:
    """Minimal standardized response format for processing"""

    success: bool
    amount: float
    status: str


class BankAPIAdapter(ABC):
    """Base adapter for standardizing external API responses"""

    def __init__(self):
        self.account_repository = AccountRepository.get_instance()

    @abstractmethod
    def process_payment(self, request_data: Dict[str, Any]) -> StandardizedResponse:
        """Process payment and return standardized response"""
        raise NotImplementedError("process_payment method must be implemented")

    @abstractmethod
    def check_balance(self, account_id: str) -> StandardizedResponse:
        """Check account balance"""
        raise NotImplementedError("check_balance method must be implemented")

    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> StandardizedResponse:
        """Process refund"""
        raise NotImplementedError("refund_payment method must be implemented")

    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> StandardizedResponse:
        """Get transaction status"""
        raise NotImplementedError("get_transaction_status method must be implemented")
