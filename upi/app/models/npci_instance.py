from typing import Optional, Dict, Any
from datetime import datetime
from uuid import uuid4
from threading import Lock
from app.models.enums import PaymentMethod
from app.adapters.base_adapter import StandardizedResponse, BankAPIAdapter
from app.adapters.bank_adapter import HDFCAdapter, SBIAdapter, ICICIAdapter


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
            # Initialize bank adapters with decorator pattern for enhanced functionality
            self.bank_adapters: Dict[str, BankAPIAdapter] = {
                "hdfc": self._create_enhanced_adapter(HDFCAdapter()),
                "sbi": self._create_enhanced_adapter(SBIAdapter()),
                "icici": self._create_enhanced_adapter(ICICIAdapter()),
            }
            # VPA to account mapping (in real implementation, this would be a database)
            self.vpa_registry = self._initialize_vpa_registry()
            self._initialized = True

    def _create_enhanced_adapter(self, adapter: BankAPIAdapter) -> BankAPIAdapter:
        """Create enhanced bank adapter with decorator pattern for logging and validation"""
        return BankAdapterDecorator(adapter)

    @classmethod
    def get_instance(cls) -> "NPCI":
        return cls._instance or cls()

    def process_payment(self, payer_vpa: str, payee_vpa: str, amount: float, payment_method: PaymentMethod) -> StandardizedResponse:
        """
        Main entry point for processing payment requests.
        Simple flow: User App → NPCI → Bank (with decorators)
        """

        try:
            print(f"🏛️ NPCI: Processing payment {payer_vpa} → {payee_vpa} (₹{amount})")

            # Step 1: Validate VPAs
            if not self._validate_vpa(payer_vpa) or not self._validate_vpa(payee_vpa):
                return self._create_error_response("Invalid VPA format", amount)

            # Step 2: Resolve VPAs to account information
            payer_info = self._resolve_vpa_to_account_info(payer_vpa)
            payee_info = self._resolve_vpa_to_account_info(payee_vpa)

            if not payer_info or not payee_info:
                return self._create_error_response("VPA resolution failed", amount)

            # Step 3: Process inter-bank payment with enhanced adapters
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
        """Process inter-bank payment using enhanced bank adapters with decorator pattern"""
        try:
            transaction_id = f"NPCI_{uuid4().hex[:8].upper()}"
            payer_bank = payer_info["bank"]
            payee_bank = payee_info["bank"]
            payer_account = payer_info["account_number"]
            payee_account = payee_info["account_number"]

            print(f"🏦 NPCI: Processing {payer_bank.upper()} → {payee_bank.upper()} transfer")

            # Step 1: Debit from payer's bank (with decorator)
            payer_adapter = self.bank_adapters[payer_bank]
            debit_request = {"account_number": payer_account, "amount": amount, "transaction_type": "DEBIT", "transaction_id": transaction_id}
            debit_response = payer_adapter.process_payment(debit_request)

            if not debit_response.success:
                print(f"❌ Debit failed from {payer_bank.upper()}")
                return self._create_error_response("Debit failed", amount)

            print(f"✅ Debit successful from {payer_bank.upper()}")

            # Step 2: Credit to payee's bank (with decorator)
            payee_adapter = self.bank_adapters[payee_bank]
            credit_request = {"account_number": payee_account, "amount": amount, "transaction_type": "CREDIT", "transaction_id": transaction_id}
            credit_response = payee_adapter.process_payment(credit_request)

            if not credit_response.success:
                print(f"❌ Credit failed to {payee_bank.upper()}")
                return self._create_error_response("Credit failed", amount)

            print(f"✅ Credit successful to {payee_bank.upper()}")
            print(f"🎉 NPCI: Payment completed successfully!")

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
            # Demo users with proper VPAs
            "Rahul Sharma@HDFC": {"account_number": "1234567890", "bank": "hdfc", "account_holder": "Rahul Sharma"},
            "Priya Patel@SBI": {"account_number": "0987654321", "bank": "sbi", "account_holder": "Priya Patel"},
            "Amit Kumar@HDFC": {"account_number": "1122334455", "bank": "hdfc", "account_holder": "Amit Kumar"},
            "Kavya Reddy@ICICI": {"account_number": "5566778899", "bank": "icici", "account_holder": "Kavya Reddy"},
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


class BankAdapterDecorator(BankAPIAdapter):
    """Decorator pattern for enhancing bank adapters with logging and validation"""

    def __init__(self, bank_adapter: BankAPIAdapter):
        self._bank_adapter = bank_adapter

    def process_payment(self, request_data: Dict[str, Any]) -> StandardizedResponse:
        """Enhanced payment processing with decorator functionality"""
        # Pre-processing: Log and validate
        print(f"🔧 Bank Adapter Decorator: Processing {request_data.get('transaction_type', 'UNKNOWN')} request")
        print(f"   Account: {request_data.get('account_number', 'N/A')}")
        print(f"   Amount: ₹{request_data.get('amount', 0.0)}")

        # Call the actual bank adapter
        response = self._bank_adapter.process_payment(request_data)

        # Post-processing: Log result
        if response.success:
            print(f"✅ Bank Adapter Decorator: {request_data.get('transaction_type', 'UNKNOWN')} successful")
        else:
            print(f"❌ Bank Adapter Decorator: {request_data.get('transaction_type', 'UNKNOWN')} failed")

        return response

    def check_balance(self, account_id: str) -> StandardizedResponse:
        """Enhanced balance check with decorator functionality"""
        print(f"🔧 Bank Adapter Decorator: Checking balance for {account_id}")
        response = self._bank_adapter.check_balance(account_id)
        print(f"✅ Bank Adapter Decorator: Balance check completed")
        return response

    def refund_payment(self, transaction_id: str, amount: float) -> StandardizedResponse:
        """Enhanced refund with decorator functionality"""
        print(f"🔧 Bank Adapter Decorator: Processing refund for {transaction_id}")
        response = self._bank_adapter.refund_payment(transaction_id, amount)
        print(f"✅ Bank Adapter Decorator: Refund processing completed")
        return response

    def get_transaction_status(self, transaction_id: str) -> StandardizedResponse:
        """Enhanced status check with decorator functionality"""
        print(f"🔧 Bank Adapter Decorator: Checking status for {transaction_id}")
        response = self._bank_adapter.get_transaction_status(transaction_id)
        print(f"✅ Bank Adapter Decorator: Status check completed")
        return response
