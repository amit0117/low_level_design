from typing import Dict, Any
from app.abstract_factories.abstract_products import BankConnector, BankAuthHandler, BankTransactionFormatter, BankNotificationAdapter


class SBIConnector(BankConnector):
    def connect(self) -> bool:
        print("Connecting to SBI Bank...")
        return True

    def make_payment(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        print(f"SBI: Paying {amount} to {to_vpa}")
        return {"status": "success", "txn_id": "SBI456"}


class SBIAuthHandler(BankAuthHandler):
    def authenticate(self, user_id: str, pin: str) -> bool:
        print(f"SBI: Authenticating {user_id}")
        return True


class SBITransactionFormatter(BankTransactionFormatter):
    def format_request(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        return {"bank": "SBI", "amount": amount, "to": to_vpa}


class SBINotificationAdapter(BankNotificationAdapter):
    def send_notification(self, message: str, user_id: str) -> bool:
        print(f"SBI Notification to {user_id}: {message}")
        return True
