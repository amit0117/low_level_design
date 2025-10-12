from datetime import datetime, timedelta
from collections import defaultdict
from app.proxies.base_proxy import PaymentProcessorProxy, PaymentProcessor
from app.adapters.base_adapter import StandardizedResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.payment import Payment


class RateLimitProxy(PaymentProcessorProxy):
    """
    Rate Limiting Proxy - ACCESS CONTROL

    Why Proxy Pattern:
    - Controls access to the payment system
    - Prevents requests from reaching core logic
    - Acts as a gatekeeper/security layer
    """

    def __init__(self, processor: PaymentProcessor):
        super().__init__(processor)
        self.request_counts = defaultdict(list)
        self.limits = {"per_minute": 5, "per_hour": 50}

    def process_payment(self, payment: "Payment") -> StandardizedResponse:
        """Block requests that exceed rate limits"""

        vpa = payment.get_payer_account().get_vpa()
        now = datetime.now()

        # Check rate limits
        if self._exceeds_rate_limit(vpa, now):
            return StandardizedResponse(success=False, amount=payment.get_amount(), status="RATE_LIMITED")

        # Record request
        self.request_counts[vpa].append(now)
        self._cleanup_old_requests(vpa, now)

        # Allow request to proceed
        return self._processor.process_payment(payment)

    def _exceeds_rate_limit(self, vpa: str, now: datetime) -> bool:
        """Check if VPA exceeds rate limits"""
        recent_requests = [req for req in self.request_counts[vpa] if now - req < timedelta(minutes=1)]
        return len(recent_requests) >= self.limits["per_minute"]

    def _cleanup_old_requests(self, vpa: str, now: datetime) -> None:
        """Remove old request records"""
        cutoff = now - timedelta(hours=1)
        self.request_counts[vpa] = [req for req in self.request_counts[vpa] if req > cutoff]
