from abc import ABC, abstractmethod
from typing import Dict, Any


class BankConnector(ABC):
    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError("connect method must be implemented")

    @abstractmethod
    def make_payment(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        raise NotImplementedError("make_payment method must be implemented")


class BankAuthHandler(ABC):
    @abstractmethod
    def authenticate(self, user_id: str, pin: str) -> bool:
        raise NotImplementedError("authenticate method must be implemented")


class BankTransactionFormatter(ABC):
    @abstractmethod
    def format_request(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        raise NotImplementedError("format_request method must be implemented")


class BankNotificationAdapter(ABC):
    @abstractmethod
    def send_notification(self, message: str, user_id: str) -> bool:
        raise NotImplementedError("send_notification method must be implemented")
