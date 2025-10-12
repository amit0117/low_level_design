from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from threading import Lock
from app.models.enums import PaymentMethod
from app.adapters.base_adapter import StandardizedResponse, BankAPIAdapter
from app.adapters.bank_adapter import HDFCAdapter, SBIAdapter


class NPCI:
    """National Payments Corporation of India - Central clearing house for UPI transactions"""

    _instance: Optional["NPCI"] = None
    _lock = Lock()

    def __new__(cls) -> "NPCI":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            # Initialize bank adapters for inter-bank communication
            self.bank_adapters: Dict[str, BankAPIAdapter] = {"hdfc": HDFCAdapter(), "sbi": SBIAdapter()}
            # VPA to account mapping (in real implementation, this would be a database)
            self.vpa_registry = self._initialize_vpa_registry()
            self._initialized = True

    @classmethod
    def get_instance(cls) -> "NPCI":
        return cls._instance or cls()

    def process_payment(self, payer_vpa: str, payee_vpa: str, amount: float, payment_method: PaymentMethod) -> StandardizedResponse:
        """
        Main entry point for processing payment requests.

        NPCI's responsibility:
        1. Validate VPAs
        2. Resolve VPAs to account numbers
        3. Coordinate inter-bank communication
        4. Handle debit/credit operations
        5. Return standardized response
        """

        try:
            # Step 1: Validate VPAs
            if not self._validate_vpa(payer_vpa) or not self._validate_vpa(payee_vpa):
                return self._create_error_response("Invalid VPA format", amount)

            # Step 2: Resolve VPAs to account information
            payer_info = self._resolve_vpa_to_account_info(payer_vpa)
            payee_info = self._resolve_vpa_to_account_info(payee_vpa)

            if not payer_info or not payee_info:
                return self._create_error_response("VPA resolution failed", amount)

            # Step 3: Process inter-bank payment
            return self._process_inter_bank_payment(payer_info, payee_info, amount)

        except Exception as e:
            return self._create_error_response(f"Payment processing failed: {str(e)}", amount)

    def process_refund(self, original_transaction_id: str, amount: float, payer_vpa: str, payee_vpa: str) -> StandardizedResponse:
        """Process refund through NPCI - reverse the original payment"""

        try:
            # Resolve VPAs to account information
            payer_info = self._resolve_vpa_to_account_info(payer_vpa)
            payee_info = self._resolve_vpa_to_account_info(payee_vpa)

            if not payer_info or not payee_info:
                return self._create_error_response("VPA resolution failed for refund", amount)

            # Process refund as reverse payment (payee -> payer)
            return self._process_inter_bank_payment(payee_info, payer_info, amount)

        except Exception as e:
            return self._create_error_response(f"Refund processing failed: {str(e)}", amount)

    def _validate_vpa(self, vpa: str) -> bool:
        """Validate VPA format"""
        if "@" not in vpa:
            return False
        name, bank = vpa.split("@", 1)
        return bool(name and bank and bank.lower() in self.bank_adapters)

    def _process_inter_bank_payment(self, payer_info: Dict[str, Any], payee_info: Dict[str, Any], amount: float) -> StandardizedResponse:
        """Process inter-bank payment using bank adapters"""
        try:
            transaction_id = f"NPCI_{uuid4().hex[:8].upper()}"
            payer_bank = payer_info["bank"]
            payee_bank = payee_info["bank"]
            payer_account = payer_info["account_number"]
            payee_account = payee_info["account_number"]

            # Step 1: Debit from payer's bank
            payer_adapter = self.bank_adapters[payer_bank]
            debit_request = {"account_number": payer_account, "amount": amount, "transaction_type": "DEBIT", "transaction_id": transaction_id}
            debit_response = payer_adapter.process_payment(debit_request)

            if not debit_response.success:
                return self._create_error_response("Debit failed", amount)

            # Step 2: Credit to payee's bank
            payee_adapter = self.bank_adapters[payee_bank]
            credit_request = {"account_number": payee_account, "amount": amount, "transaction_type": "CREDIT", "transaction_id": transaction_id}
            credit_response = payee_adapter.process_payment(credit_request)

            if not credit_response.success:
                return self._create_error_response("Credit failed", amount)

            # Step 3: Both operations successful

            return StandardizedResponse(
                success=True,
                amount=amount,
                status="SUCCESS",
            )

        except Exception as e:
            return self._create_error_response(f"Inter-bank payment failed: {str(e)}", amount)

    def _initialize_vpa_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize VPA to account mapping registry"""
        return {
            "amit@hdfc": {"account_number": "HDFC12345", "bank": "hdfc", "account_holder": "Amit Kumar"},
            "priya@sbi": {"account_number": "SBI67890", "bank": "sbi", "account_holder": "Priya Sharma"},
            "rajesh@hdfc": {"account_number": "HDFC54321", "bank": "hdfc", "account_holder": "Rajesh Patel"},
            "shopkeeper@sbi": {"account_number": "SBI98765", "bank": "sbi", "account_holder": "Shopkeeper"},
        }

    def _resolve_vpa_to_account_info(self, vpa: str) -> Optional[Dict[str, Any]]:
        """Resolve VPA to complete account information"""
        return self.vpa_registry.get(vpa)

    def _create_error_response(self, message: str, amount: float) -> StandardizedResponse:
        """Create standardized error response"""
        return StandardizedResponse(
            success=False,
            amount=amount,
            status="FAILED",
        )
