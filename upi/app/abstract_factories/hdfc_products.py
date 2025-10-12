from typing import Dict, Any
from app.abstract_factories.abstract_products import BankConnector, BankAuthHandler, BankTransactionFormatter, BankNotificationAdapter


class HDFCConnector(BankConnector):
    def connect(self) -> bool:
        print("Connecting to HDFC Bank...")
        return True

    def make_payment(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        print(f"HDFC: Paying {amount} to {to_vpa}")
        return {"status": "success", "txn_id": "HDFC123"}


class HDFCAuthHandler(BankAuthHandler):
    def authenticate(self, user_id: str, pin: str) -> bool:
        print(f"HDFC: Authenticating {user_id}")
        return True


class HDFCTransactionFormatter(BankTransactionFormatter):
    def format_request(self, amount: float, to_vpa: str) -> Dict[str, Any]:
        return {"bank": "HDFC", "amount": amount, "to": to_vpa}


class HDFCNotificationAdapter(BankNotificationAdapter):
    def send_notification(self, message: str, user_id: str) -> bool:
        print(f"HDFC Notification to {user_id}: {message}")
        return True
