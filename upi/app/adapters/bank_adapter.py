from typing import Dict, Any
from datetime import datetime
from app.adapters.base_adapter import BankAPIAdapter, StandardizedResponse


class HDFCAdapter(BankAPIAdapter):
    """Adapter for HDFC Bank API responses"""

    def process_payment(self, request_data: Dict[str, Any]) -> StandardizedResponse:
        """Process HDFC payment and standardize response"""
        try:
            hdfc_response = self._call_hdfc_api(request_data)

            return StandardizedResponse(
                success=hdfc_response.get("responseCode") == "00",
                amount=request_data.get("amount", 0.0),
                status="SUCCESS" if hdfc_response.get("responseCode") == "00" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(request_data.get("amount", 0.0), str(e))

    def check_balance(self, account_id: str) -> StandardizedResponse:
        """Check HDFC account balance"""
        try:
            balance_response = self._call_hdfc_balance_api(account_id)

            return StandardizedResponse(
                success=balance_response.get("responseCode") == "00",
                amount=balance_response.get("availableBalance", 0.0),
                status="SUCCESS" if balance_response.get("responseCode") == "00" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(0.0, str(e))

    def refund_payment(self, transaction_id: str, amount: float) -> StandardizedResponse:
        """Process HDFC refund"""
        try:
            refund_response = self._call_hdfc_refund_api(transaction_id, amount)

            return StandardizedResponse(
                success=refund_response.get("responseCode") == "00",
                amount=amount,
                status="SUCCESS" if refund_response.get("responseCode") == "00" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(amount, str(e))

    def get_transaction_status(self, transaction_id: str) -> StandardizedResponse:
        """Get HDFC transaction status"""
        try:
            status_response = self._call_hdfc_status_api(transaction_id)

            return StandardizedResponse(
                success=status_response.get("responseCode") == "00",
                amount=0.0,
                status=status_response.get("transactionStatus", "UNKNOWN"),
            )
        except Exception as e:
            return self._create_error_response(0.0, str(e))

    def _create_error_response(self, amount: float, error_message: str) -> StandardizedResponse:
        """Create standardized error response"""
        return StandardizedResponse(
            success=False,
            amount=amount,
            status="FAILED",
        )

    def _call_hdfc_api(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process HDFC payment with actual debit/credit operations"""
        try:
            # Extract payment details
            account_number = request_data.get("account_number", "")
            amount = request_data.get("amount", 0.0)
            transaction_type = request_data.get("transaction_type", "")

            # Get account from repository
            account = self.account_repository.get_account(account_number)
            if not account:
                return {
                    "responseCode": "99",
                    "responseMessage": f"Account not found: {account_number}",
                    "transactionId": "",
                    "referenceNumber": "",
                    "hdfcReference": "",
                    "error": "Account not found",
                }

            hdfc_transaction_id = f"HDFC_{hash(str(request_data)) % 1000000:06d}"

            if transaction_type == "DEBIT":
                # Check sufficient funds and debit
                if account.get_balance() < amount:
                    return {
                        "responseCode": "99",
                        "responseMessage": "Insufficient funds",
                        "transactionId": "",
                        "referenceNumber": "",
                        "hdfcReference": "",
                        "error": "Insufficient funds",
                    }
                account.withdraw(amount)

            elif transaction_type == "CREDIT":
                # Credit the amount
                account.deposit(amount)

            # Update account in repository
            self.account_repository.update_account(account)

            return {
                "responseCode": "00",
                "responseMessage": f"HDFC {transaction_type} transaction successful",
                "transactionId": hdfc_transaction_id,
                "referenceNumber": f"HDFC_REF_{hash(str(request_data)) % 10000:04d}",
                "hdfcReference": f"HDFC_REF_{hash(str(request_data)) % 100000:05d}",
                "accountNumber": account_number,
                "amount": amount,
                "transactionType": transaction_type,
            }
        except Exception as e:
            return {
                "responseCode": "99",
                "responseMessage": f"Transaction failed: {str(e)}",
                "transactionId": "",
                "referenceNumber": "",
                "hdfcReference": "",
                "error": str(e),
            }

    def _call_hdfc_balance_api(self, account_id: str) -> Dict[str, Any]:
        """Get HDFC account balance from repository"""
        account = self.account_repository.get_account(account_id)
        if not account:
            return {
                "responseCode": "99",
                "responseMessage": f"Account not found: {account_id}",
                "availableBalance": 0.0,
                "referenceNumber": "",
                "error": "Account not found",
            }

        return {
            "responseCode": "00",
            "responseMessage": "Balance retrieved successfully",
            "availableBalance": account.get_balance(),
            "referenceNumber": f"HDFC_BAL_{hash(account_id) % 10000:04d}",
        }

    def _call_hdfc_refund_api(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Process HDFC refund - this will be handled by NPCI with proper account info"""
        try:
            refund_id = f"HDFC_REFUND_{hash(transaction_id) % 1000000:06d}"

            # Refund processing is handled by NPCI with proper account information
            # This method is kept for compatibility but actual refund logic is in NPCI

            return {
                "responseCode": "00",
                "responseMessage": "Refund processed successfully",
                "refundTransactionId": refund_id,
                "referenceNumber": f"HDFC_REFUNDREF_{hash(transaction_id) % 10000:04d}",
                "refundAmount": amount,
                "originalTransactionId": transaction_id,
            }
        except Exception as e:
            return {
                "responseCode": "99",
                "responseMessage": f"Refund failed: {str(e)}",
                "refundTransactionId": "",
                "referenceNumber": "",
                "error": str(e),
            }

    def _call_hdfc_status_api(self, transaction_id: str) -> Dict[str, Any]:
        """Simulate HDFC status API call"""
        return {
            "responseCode": "00",
            "responseMessage": "Transaction status retrieved",
            "transactionStatus": "SUCCESS",
            "referenceNumber": f"HDFC_STATUS_{hash(transaction_id) % 10000:04d}",
        }


class SBIAdapter(BankAPIAdapter):
    """Adapter for SBI Bank API responses"""

    def process_payment(self, request_data: Dict[str, Any]) -> StandardizedResponse:
        """Process SBI payment and standardize response"""
        try:
            sbi_response = self._call_sbi_api(request_data)

            return StandardizedResponse(
                success=sbi_response.get("statusCode") == "200",
                amount=request_data.get("amount", 0.0),
                status="SUCCESS" if sbi_response.get("statusCode") == "200" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(request_data.get("amount", 0.0), str(e))

    def check_balance(self, account_id: str) -> StandardizedResponse:
        """Check SBI account balance"""
        try:
            balance_response = self._call_sbi_balance_api(account_id)

            return StandardizedResponse(
                success=balance_response.get("statusCode") == "200",
                amount=balance_response.get("currentBalance", 0.0),
                status="SUCCESS" if balance_response.get("statusCode") == "200" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(0.0, str(e))

    def refund_payment(self, transaction_id: str, amount: float) -> StandardizedResponse:
        """Process SBI refund"""
        try:
            refund_response = self._call_sbi_refund_api(transaction_id, amount)

            return StandardizedResponse(
                success=refund_response.get("statusCode") == "200",
                amount=amount,
                status="SUCCESS" if refund_response.get("statusCode") == "200" else "FAILED",
            )
        except Exception as e:
            return self._create_error_response(amount, str(e))

    def get_transaction_status(self, transaction_id: str) -> StandardizedResponse:
        """Get SBI transaction status"""
        try:
            status_response = self._call_sbi_status_api(transaction_id)

            return StandardizedResponse(
                success=status_response.get("statusCode") == "200",
                amount=0.0,
                status=status_response.get("transactionStatus", "UNKNOWN"),
            )
        except Exception as e:
            return self._create_error_response(0.0, str(e))

    def _create_error_response(self, amount: float, error_message: str) -> StandardizedResponse:
        """Create standardized error response"""
        return StandardizedResponse(
            success=False,
            amount=amount,
            status="FAILED",
        )

    def _call_sbi_api(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process SBI payment with actual debit/credit operations"""
        try:
            # Extract payment details
            account_number = request_data.get("account_number", "")
            amount = request_data.get("amount", 0.0)
            transaction_type = request_data.get("transaction_type", "")
            transaction_id = request_data.get("transaction_id", "")

            # Get account from repository
            account = self.account_repository.get_account(account_number)
            if not account:
                return {
                    "statusCode": "500",
                    "statusMessage": f"Account not found: {account_number}",
                    "sbiTransactionId": "",
                    "sbiReferenceId": "",
                    "error": "Account not found",
                }

            sbi_transaction_id = f"SBI_{hash(str(request_data)) % 1000000:06d}"

            if transaction_type == "DEBIT":
                # Check sufficient funds and debit
                if account.get_balance() < amount:
                    return {
                        "statusCode": "500",
                        "statusMessage": "Insufficient funds",
                        "sbiTransactionId": "",
                        "sbiReferenceId": "",
                        "error": "Insufficient funds",
                    }
                account.withdraw(amount)

            elif transaction_type == "CREDIT":
                # Credit the amount
                account.deposit(amount)

            # Update account in repository
            self.account_repository.update_account(account)

            return {
                "statusCode": "200",
                "statusMessage": f"SBI {transaction_type} transaction processed successfully",
                "sbiTransactionId": sbi_transaction_id,
                "sbiReferenceId": f"SBI_REF_{hash(str(request_data)) % 10000:04d}",
                "accountNumber": account_number,
                "amount": amount,
                "transactionType": transaction_type,
            }
        except Exception as e:
            return {
                "statusCode": "500",
                "statusMessage": f"Transaction failed: {str(e)}",
                "sbiTransactionId": "",
                "sbiReferenceId": "",
                "error": str(e),
            }

    def _call_sbi_balance_api(self, account_id: str) -> Dict[str, Any]:
        """Get SBI account balance from repository"""
        account = self.account_repository.get_account(account_id)
        if not account:
            return {
                "statusCode": "500",
                "statusMessage": f"Account not found: {account_id}",
                "currentBalance": 0.0,
                "sbiReferenceId": "",
                "error": "Account not found",
            }

        return {
            "statusCode": "200",
            "statusMessage": "Balance inquiry successful",
            "currentBalance": account.get_balance(),
            "sbiReferenceId": f"SBI_BAL_{hash(account_id) % 10000:04d}",
        }

    def _call_sbi_refund_api(self, transaction_id: str, amount: float) -> Dict[str, Any]:
        """Process SBI refund - this will be handled by NPCI with proper account info"""
        try:
            refund_id = f"SBI_REFUND_{hash(transaction_id) % 1000000:06d}"

            # Refund processing is handled by NPCI with proper account information
            # This method is kept for compatibility but actual refund logic is in NPCI

            return {
                "statusCode": "200",
                "statusMessage": "Refund processed successfully",
                "sbiRefundId": refund_id,
                "sbiReferenceId": f"SBI_REFUNDREF_{hash(transaction_id) % 10000:04d}",
                "refundAmount": amount,
                "originalTransactionId": transaction_id,
            }
        except Exception as e:
            return {"statusCode": "500", "statusMessage": f"Refund failed: {str(e)}", "sbiRefundId": "", "sbiReferenceId": "", "error": str(e)}

    def _call_sbi_status_api(self, transaction_id: str) -> Dict[str, Any]:
        """Simulate SBI status API call"""
        return {
            "statusCode": "200",
            "statusMessage": "Transaction status retrieved",
            "transactionStatus": "SUCCESS",
            "sbiReferenceId": f"SBI_STATUS_{hash(transaction_id) % 10000:04d}",
        }
