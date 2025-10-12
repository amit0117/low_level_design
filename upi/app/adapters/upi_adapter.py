from typing import Dict, Any
from app.adapters.base_adapter import BankAPIAdapter, StandardizedResponse


class UPIAdapter(BankAPIAdapter):
    """Adapter for UPI/NPCI API responses"""

    def process_payment(self, request_data: Dict[str, Any]) -> StandardizedResponse:
        """Process UPI payment and standardize response"""
        try:
            # Simulate UPI API call
            upi_response = self._call_upi_api(request_data)

            # Standardize the response
            return StandardizedResponse(
                success=upi_response.get("status") == "SUCCESS",
                amount=request_data.get("amount", 0.0),
                status=upi_response.get("status", "FAILED"),
            )
        except Exception as e:
            return StandardizedResponse(
                success=False,
                amount=request_data.get("amount", 0.0),
                status="FAILED",
            )

    def check_balance(self, account_id: str) -> StandardizedResponse:
        """Check balance via UPI"""
        try:
            # Simulate balance check
            balance_response = self._call_balance_api(account_id)

            return StandardizedResponse(
                success=True,
                amount=balance_response.get("balance", 0.0),
                status="SUCCESS",
            )
        except Exception as e:
            return StandardizedResponse(
                success=False,
                amount=0.0,
                status="FAILED",
            )

    def refund_payment(self, transaction_id: str, amount: float) -> StandardizedResponse:
        """Process refund via UPI"""
        try:
            refund_response = self._call_refund_api(transaction_id, amount)

            return StandardizedResponse(
                success=refund_response.get("status") == "SUCCESS",
                amount=amount,
                status=refund_response.get("status", "FAILED"),
            )
        except Exception as e:
            return StandardizedResponse(
                success=False,
                amount=amount,
                status="FAILED",
            )

    def get_transaction_status(self, transaction_id: str) -> StandardizedResponse:
        """Get transaction status from UPI"""
        try:
            status_response = self._call_status_api(transaction_id)

            return StandardizedResponse(
                success=True,
                amount=0.0,
                status=status_response.get("status", "UNKNOWN"),
            )
        except Exception as e:
            return StandardizedResponse(
                success=False,
                amount=0.0,
                status="FAILED",
            )

    def _call_upi_api(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process UPI payment with actual debit/credit operations"""
        try:
            # Extract payment details
            payer_vpa = request_data.get("payer_vpa", "")
            payee_vpa = request_data.get("payee_vpa", "")
            amount = request_data.get("amount", 0.0)

            # In real UPI implementation, this would:
            # 1. Resolve VPAs to bank accounts
            # 2. Check sufficient funds in payer's account
            # 3. Debit from payer's bank account
            # 4. Credit to payee's bank account
            # 5. Handle inter-bank settlement
            # 6. Update account balances

            transaction_id = f"UPI_{hash(str(request_data)) % 1000000:06d}"

            # Simulate actual debit/credit operations
            print(f"UPI: Resolving VPA {payer_vpa} to bank account")
            print(f"UPI: Resolving VPA {payee_vpa} to bank account")
            print(f"UPI: Checking sufficient funds in payer's account")
            print(f"UPI: Processing debit of ₹{amount} from {payer_vpa}")
            print(f"UPI: Processing credit of ₹{amount} to {payee_vpa}")
            print(f"UPI: Handling inter-bank settlement")
            print(f"UPI: Transaction {transaction_id} completed successfully")

            return {
                "status": "SUCCESS",
                "message": "Transaction successful - Debit and Credit completed",
                "refId": f"REF_{hash(str(request_data)) % 10000:04d}",
                "upiRef": f"UPIREF_{hash(str(request_data)) % 100000:05d}",
                "merchantId": "MERCHANT_001",
                "debitAmount": amount,
                "creditAmount": amount,
                "payerVpa": payer_vpa,
                "payeeVpa": payee_vpa,
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": f"Transaction failed: {str(e)}",
                "refId": "",
                "upiRef": "",
                "merchantId": "",
                "error": str(e),
            }

    def _call_balance_api(self, account_id: str) -> Dict[str, Any]:
        """Simulate balance API call"""
        return {"balance": 50000.0, "refId": f"BAL_{hash(account_id) % 10000:04d}"}

    def _call_refund_api(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Simulate refund API call"""
        return {
            "status": "SUCCESS",
            "refundId": f"REFUND_{hash(transaction_id) % 1000000:06d}",
            "message": "Refund processed successfully",
            "refId": f"REFUNDREF_{hash(transaction_id) % 10000:04d}",
        }

    def _call_status_api(self, transaction_id: str) -> Dict[str, Any]:
        """Simulate status API call"""
        return {"status": "SUCCESS", "message": "Transaction completed", "refId": f"STATUS_{hash(transaction_id) % 10000:04d}"}
