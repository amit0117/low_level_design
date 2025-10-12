from app.services.payment_service import PaymentService
from app.models.user import User
from app.models.account import Account
from app.models.payment import Payment
from app.models.enums import PaymentMethod, AccountType, Currency, PaymentType
from app.repositories.user_respository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.adapters.base_adapter import StandardizedResponse
from app.commands.command_invoker import CommandInvoker
from app.models.npci_instance import NPCI
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from collections import defaultdict


class NPCIProxy:
    """Proxy pattern for NPCI with fraud detection and security checks"""

    def __init__(self, npci: NPCI):
        self._npci = npci
        self.fraud_threshold = 50000.0  # ₹50,000 threshold for fraud detection
        self.suspicious_transactions = []

    def process_payment(self, payer_vpa: str, payee_vpa: str, amount: float, payment_method: PaymentMethod) -> StandardizedResponse:
        """Enhanced payment processing with fraud detection"""
        print(f"🛡️ NPCI Proxy: Fraud detection check for ₹{amount}")

        # Fraud detection checks
        if self._is_suspicious_transaction(payer_vpa, payee_vpa, amount):
            print(f"🚨 NPCI Proxy: Suspicious transaction detected!")
            print(f"   Amount: ₹{amount} (above threshold ₹{self.fraud_threshold})")
            print(f"   From: {payer_vpa}")
            print(f"   To: {payee_vpa}")

            # Log suspicious transaction
            self.suspicious_transactions.append(
                {"payer_vpa": payer_vpa, "payee_vpa": payee_vpa, "amount": amount, "timestamp": datetime.now(), "reason": "High value transaction"}
            )

            # For demo, allow but flag as suspicious
            print(f"⚠️ NPCI Proxy: Allowing transaction but flagging as suspicious")

        # Additional security checks
        if self._is_rapid_transaction(payer_vpa):
            print(f"⚡ NPCI Proxy: Rapid transaction detected for {payer_vpa}")
            print(f"⚠️ NPCI Proxy: Allowing but monitoring")

        # Call actual NPCI
        print(f"🔄 NPCI Proxy: Forwarding to actual NPCI...")
        return self._npci.process_payment(payer_vpa, payee_vpa, amount, payment_method)

    def _is_suspicious_transaction(self, payer_vpa: str, payee_vpa: str, amount: float) -> bool:
        """Check if transaction is suspicious"""
        return amount > self.fraud_threshold

    def _is_rapid_transaction(self, payer_vpa: str) -> bool:
        """Check for rapid successive transactions"""
        # Simple check - in real implementation, this would be more sophisticated
        return False

    def get_suspicious_transactions(self) -> List[Dict]:
        """Get list of suspicious transactions"""
        return self.suspicious_transactions


class UPIApp:
    def __init__(self):
        self.payment_service = PaymentService()
        self.user_repository = UserRepository()
        self.account_repository = AccountRepository()
        self.command_invoker = CommandInvoker()

        # Initialize NPCI with proxy for fraud detection
        self.npci = NPCI.get_instance()
        self.npci_proxy = NPCIProxy(self.npci)

        # Rate limiting at application level
        self.request_counts: Dict[str, List[datetime]] = defaultdict(list)
        self.rate_limits = {"per_minute": 5, "per_hour": 50}

    def register_user(self, name: str, phone: str, email: str) -> str:
        user = User(name, phone, email)
        self.user_repository.add_user(user)
        return user.get_id()

    def create_account(self, user_id: str, bank_name: str, account_number: str) -> str:
        user = self.user_repository.get_user(user_id)
        account = Account(account_number, AccountType.SAVINGS, 10000.0, user, bank_name)
        self.account_repository.add_account(account)
        return account.get_vpa()

    def send_money(
        self, payer_vpa: str, payee_vpa: str, amount: float, payment_method: PaymentMethod = PaymentMethod.UPI_PUSH
    ) -> StandardizedResponse:
        print(f"📱 UPI App: User request to send ₹{amount} from {payer_vpa} to {payee_vpa}")

        # Rate limiting check
        if self._is_rate_limited(payer_vpa):
            return StandardizedResponse(success=False, amount=amount, status="RATE_LIMITED")

        # Record request
        self._record_request(payer_vpa)

        # Process payment through proxy (User App → Proxy → NPCI → Bank)
        payer_account = self.account_repository.get_account_by_vpa(payer_vpa)
        payee_account = self.account_repository.get_account_by_vpa(payee_vpa)

        payment = Payment(PaymentType.DEBIT, payment_method, amount, payer_account, payee_account, Currency.INR)

        # Use proxy for fraud detection before NPCI
        print(f"🔄 UPI App: Processing through fraud detection proxy...")
        return self.npci_proxy.process_payment(payer_vpa, payee_vpa, amount, payment_method)

    def request_money(self, requester_vpa: str, payer_vpa: str, amount: float) -> StandardizedResponse:
        return self.send_money(payer_vpa, requester_vpa, amount, PaymentMethod.UPI_PULL)

    def check_balance(self, vpa: str) -> float:
        account = self.account_repository.get_account_by_vpa(vpa)
        return account.get_balance()

    def get_transaction_history(self, vpa: str) -> List[dict]:
        account = self.account_repository.get_account_by_vpa(vpa)
        return account.get_transaction_history()

    def get_user_info(self, user_id: str) -> Optional[dict]:
        user = self.user_repository.get_user(user_id)
        if not user:
            return None
        return {"user_id": user.get_id(), "name": user.get_name(), "email": user.get_email()}

    def get_account_info(self, vpa: str) -> Optional[dict]:
        account = self.account_repository.get_account_by_vpa(vpa)
        if not account:
            return None
        return {
            "vpa": account.get_vpa(),
            "bank_name": account.get_bank_name(),
            "account_number": account.get_account_number(),
            "balance": account.get_balance(),
            "user_name": account.get_user().get_name(),
        }

    def _is_rate_limited(self, vpa: str) -> bool:
        """Check if VPA exceeds rate limits"""
        now = datetime.now()
        recent_requests = [req for req in self.request_counts[vpa] if now - req < timedelta(minutes=1)]
        return len(recent_requests) >= self.rate_limits["per_minute"]

    def _record_request(self, vpa: str) -> None:
        """Record request for rate limiting"""
        now = datetime.now()
        self.request_counts[vpa].append(now)

        # Cleanup old requests
        cutoff = now - timedelta(hours=1)
        self.request_counts[vpa] = [req for req in self.request_counts[vpa] if req > cutoff]

    def get_suspicious_transactions(self) -> List[Dict]:
        """Get list of suspicious transactions detected by fraud detection proxy"""
        return self.npci_proxy.get_suspicious_transactions()
