from app.services.payment_service import PaymentService
from app.models.user import User
from app.models.account import Account
from app.models.payment import Payment
from app.models.enums import PaymentMethod, AccountType, Currency, PaymentType
from app.repositories.user_respository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.adapters.base_adapter import StandardizedResponse
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from collections import defaultdict


class UPIApp:
    def __init__(self):
        self.payment_service = PaymentService()
        self.user_repository = UserRepository()
        self.account_repository = AccountRepository()

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
        # Rate limiting check
        if self._is_rate_limited(payer_vpa):
            return StandardizedResponse(success=False, amount=amount, status="RATE_LIMITED")

        # Record request
        self._record_request(payer_vpa)

        # Process payment
        payer_account = self.account_repository.get_account_by_vpa(payer_vpa)
        payee_account = self.account_repository.get_account_by_vpa(payee_vpa)

        payment = Payment(PaymentType.DEBIT, payment_method, amount, payer_account, payee_account, Currency.INR)
        return self.payment_service.process_payment(payment)

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
