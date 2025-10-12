from typing import Dict, Set, TYPE_CHECKING
from datetime import datetime, timedelta
from app.decorators.base_decorator import PaymentProcessorDecorator
from app.adapters.base_adapter import StandardizedResponse
from app.models.enums import PaymentMethod

if TYPE_CHECKING:
    from app.models.payment import Payment


class FraudCheckDecorator(PaymentProcessorDecorator):
    """Decorator to add fraud detection to payment processing"""

    def __init__(self, processor):
        super().__init__(processor)
        # Track suspicious activities
        self.suspicious_vpas: Set[str] = set()
        self.transaction_history: Dict[str, list] = {}  # VPA -> list of transactions
        self.blocked_vpas: Set[str] = set()

        # Fraud detection thresholds
        self.MAX_DAILY_AMOUNT = 100000.0  # ₹1 lakh per day
        self.MAX_HOURLY_TRANSACTIONS = 10  # 10 transactions per hour
        self.SUSPICIOUS_AMOUNT_THRESHOLD = 50000.0  # ₹50k single transaction

    def process_payment(self, payment) -> StandardizedResponse:
        """Process payment with fraud checks"""

        # Check if VPA is blocked
        payer_vpa = payment.get_payer_account().get_vpa()
        if payer_vpa in self.blocked_vpas:
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="BLOCKED")

        # Perform fraud checks
        fraud_check_result = self._perform_fraud_checks(payment)
        if not fraud_check_result["is_safe"]:
            # Mark as suspicious and block if severe
            self.suspicious_vpas.add(payer_vpa)
            if fraud_check_result["severity"] == "HIGH":
                self.blocked_vpas.add(payer_vpa)

            return StandardizedResponse(success=False, amount=payment.get_amount(), status="FRAUD_DETECTED")

        # Update transaction history
        self._update_transaction_history(payment)

        # Process payment through wrapped processor
        return self._processor.process_payment(payment)

    def _perform_fraud_checks(self, payment) -> Dict[str, any]:
        """Perform comprehensive fraud checks"""
        payer_vpa = payment.get_payer_account().get_vpa()
        amount = payment.get_amount()
        current_time = datetime.now()

        # Check 1: Suspicious amount threshold
        if amount > self.SUSPICIOUS_AMOUNT_THRESHOLD:
            return {"is_safe": False, "severity": "HIGH", "reason": "Amount exceeds suspicious threshold"}

        # Check 2: Daily amount limit
        daily_amount = self._get_daily_transaction_amount(payer_vpa, current_time)
        if daily_amount + amount > self.MAX_DAILY_AMOUNT:
            return {"is_safe": False, "severity": "MEDIUM", "reason": "Daily amount limit exceeded"}

        # Check 3: Hourly transaction frequency
        hourly_count = self._get_hourly_transaction_count(payer_vpa, current_time)
        if hourly_count >= self.MAX_HOURLY_TRANSACTIONS:
            return {"is_safe": False, "severity": "HIGH", "reason": "Too many transactions in short time"}

        # Check 4: Payment method risk assessment
        if not self._is_payment_method_safe(payment.get_payment_method()):
            return {"is_safe": False, "severity": "LOW", "reason": "Risky payment method"}

        # Check 5: Velocity check (rapid successive transactions)
        if self._is_velocity_suspicious(payer_vpa, current_time):
            return {"is_safe": False, "severity": "MEDIUM", "reason": "Suspicious transaction velocity"}

        return {"is_safe": True, "severity": "NONE", "reason": "All checks passed"}

    def _get_daily_transaction_amount(self, vpa: str, current_time: datetime) -> float:
        """Get total transaction amount for the day"""
        if vpa not in self.transaction_history:
            return 0.0

        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_amount = 0.0

        for transaction in self.transaction_history[vpa]:
            if transaction["timestamp"] >= today_start:
                daily_amount += transaction["amount"]

        return daily_amount

    def _get_hourly_transaction_count(self, vpa: str, current_time: datetime) -> int:
        """Get transaction count in the last hour"""
        if vpa not in self.transaction_history:
            return 0

        hour_start = current_time - timedelta(hours=1)
        count = 0

        for transaction in self.transaction_history[vpa]:
            if transaction["timestamp"] >= hour_start:
                count += 1

        return count

    def _is_payment_method_safe(self, payment_method: PaymentMethod) -> bool:
        """Check if payment method is considered safe"""
        # UPI methods are generally safer than card payments
        safe_methods = {PaymentMethod.UPI_PUSH, PaymentMethod.UPI_PULL}
        return payment_method in safe_methods

    def _is_velocity_suspicious(self, vpa: str, current_time: datetime) -> bool:
        """Check for suspicious transaction velocity"""
        if vpa not in self.transaction_history:
            return False

        # Check for more than 3 transactions in last 5 minutes
        five_minutes_ago = current_time - timedelta(minutes=5)
        recent_count = 0

        for transaction in self.transaction_history[vpa]:
            if transaction["timestamp"] >= five_minutes_ago:
                recent_count += 1

        return recent_count >= 3

    def _update_transaction_history(self, payment) -> None:
        """Update transaction history for fraud analysis"""
        payer_vpa = payment.get_payer_account().get_vpa()

        if payer_vpa not in self.transaction_history:
            self.transaction_history[payer_vpa] = []

        self.transaction_history[payer_vpa].append(
            {
                "timestamp": datetime.now(),
                "amount": payment.get_amount(),
                "payee_vpa": payment.get_payee_account().get_vpa(),
                "payment_method": payment.get_payment_method().value,
            }
        )

        # Keep only last 100 transactions per VPA to manage memory
        if len(self.transaction_history[payer_vpa]) > 100:
            self.transaction_history[payer_vpa] = self.transaction_history[payer_vpa][-100:]

    def get_fraud_stats(self) -> Dict[str, any]:
        """Get fraud detection statistics"""
        return {
            "suspicious_vpas_count": len(self.suspicious_vpas),
            "blocked_vpas_count": len(self.blocked_vpas),
            "total_tracked_vpas": len(self.transaction_history),
            "suspicious_vpas": list(self.suspicious_vpas),
            "blocked_vpas": list(self.blocked_vpas),
        }

    def unblock_vpa(self, vpa: str) -> bool:
        """Unblock a VPA (admin function)"""
        if vpa in self.blocked_vpas:
            self.blocked_vpas.remove(vpa)
            return True
        return False
