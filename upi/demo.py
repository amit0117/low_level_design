from upi_app import UPIApp
from app.abstract_factories.concrete_bank_factories import HDFCFactory, SBIFactory
from app.models.enums import PaymentMethod, PaymentType, Currency, TransactionStatus, PaymentStatus
from app.adapters.bank_adapter import HDFCAdapter, SBIAdapter
from app.adapters.upi_adapter import UPIAdapter
from app.observers.payment_observer import PaymentObserver
from app.observers.transaction_observer import TransactionObserver
from app.observers.account_observer import AccountObserver
from app.states.transaction_state import TransactionState, PendingState, SuccessState, FailedState
from app.commands.command_invoker import CommandInvoker
from app.strategies.payment_strategies import CreditCardStrategy, UPIPushStrategy
from app.decorators.fraud_check_decorator import FraudCheckDecorator
from app.proxies.rate_limit_proxy import RateLimitProxy
from app.chain.chain_factory import PaymentChainFactory
from app.models.transaction import Transaction
from app.models.payment import Payment
from app.exceptions.insufficient_fund import InsufficientFundsException
import time


class ConcretePaymentObserver(PaymentObserver):
    def update_on_payment(self, payment):
        print(f"Payment Observer: Payment {payment.get_payment_id()} status updated")


class ConcreteTransactionObserver(TransactionObserver):
    def update_on_transaction(self, transaction):
        print(f"Transaction Observer: Transaction {transaction.get_transaction_id()} status updated")

    def update_on_payment(self, payment):
        print(f"Transaction Observer: Payment {payment.get_payment_id()} status updated")


class ConcreteAccountObserver(AccountObserver):
    def update_on_account_balance_change(self, account, amount, payment_type):
        print(f"Account Observer: Account {account.get_vpa()} balance changed by ₹{amount} ({payment_type.value})")


class UPIDemo:
    def __init__(self):
        self.upi_app = UPIApp()
        self.hdfc_factory = HDFCFactory()
        self.sbi_factory = SBIFactory()
        self.command_invoker = CommandInvoker()
        self.setup_observers()
        self.setup_users()

    def setup_observers(self):
        self.payment_observer = ConcretePaymentObserver()
        self.transaction_observer = ConcreteTransactionObserver()

    def setup_users(self):
        print("Setting up users and accounts...")

        self.rahul_id = self.upi_app.register_user("Rahul Sharma", "9876543210", "rahul@email.com")
        self.priya_id = self.upi_app.register_user("Priya Patel", "9876543211", "priya@email.com")
        self.amit_id = self.upi_app.register_user("Amit Kumar", "9876543212", "amit@email.com")

        self.rahul_vpa = self.upi_app.create_account(self.rahul_id, "HDFC", "1234567890")
        self.priya_vpa = self.upi_app.create_account(self.priya_id, "SBI", "0987654321")
        self.amit_vpa = self.upi_app.create_account(self.amit_id, "HDFC", "1122334455")

        print(f"Rahul (HDFC): {self.rahul_vpa}")
        print(f"Priya (SBI): {self.priya_vpa}")
        print(f"Amit (HDFC): {self.amit_vpa}")

    def demo_cross_bank_transfer(self):
        print("\n=== Cross-Bank Transfer Demo ===")

        hdfc_adapter = HDFCAdapter()
        sbi_adapter = SBIAdapter()

        print(f"Rahul balance: ₹{self.upi_app.check_balance(self.rahul_vpa)}")
        print(f"Priya balance: ₹{self.upi_app.check_balance(self.priya_vpa)}")

        print("Processing cross-bank transfer...")
        response = self.upi_app.send_money(self.rahul_vpa, self.priya_vpa, 1000.0)
        print(f"Transfer result: {response.status}")

        print(f"After transfer - Rahul: ₹{self.upi_app.check_balance(self.rahul_vpa)}")
        print(f"After transfer - Priya: ₹{self.upi_app.check_balance(self.priya_vpa)}")

    def demo_money_request(self):
        print("\n=== Money Request Demo ===")

        print(f"Amit balance: ₹{self.upi_app.check_balance(self.amit_vpa)}")
        print(f"Priya balance: ₹{self.upi_app.check_balance(self.priya_vpa)}")

        print("Processing money request...")
        response = self.upi_app.request_money(self.amit_vpa, self.priya_vpa, 500.0)
        print(f"Request result: {response.status}")

        print(f"After request - Amit: ₹{self.upi_app.check_balance(self.amit_vpa)}")
        print(f"After request - Priya: ₹{self.upi_app.check_balance(self.priya_vpa)}")

    def demo_credit_card_payment(self):
        print("\n=== Credit Card Payment Demo ===")

        credit_strategy = CreditCardStrategy()
        upi_strategy = UPIPushStrategy()

        print("Processing credit card payment...")
        response = self.upi_app.send_money(self.rahul_vpa, self.priya_vpa, 2000.0, PaymentMethod.CREDIT_CARD)
        print(f"Credit card payment result: {response.status}")

        print("Processing UPI payment...")
        response = self.upi_app.send_money(self.priya_vpa, self.amit_vpa, 1500.0, PaymentMethod.UPI_PUSH)
        print(f"UPI payment result: {response.status}")

    def demo_fraud_detection(self):
        print("\n=== Fraud Detection Demo ===")

        print("Attempting suspicious high-value transaction...")
        response = self.upi_app.send_money(self.rahul_vpa, self.priya_vpa, 60000.0)
        print(f"High-value transaction result: {response.status}")

        print("Attempting rapid successive transactions...")
        for i in range(4):
            response = self.upi_app.send_money(self.rahul_vpa, self.priya_vpa, 100.0)
            print(f"Transaction {i+1}: {response.status}")
            time.sleep(0.1)

    def demo_transaction_states(self):
        print("\n=== Transaction States Demo ===")

        # Show different states available
        pending_state = PendingState()
        success_state = SuccessState()
        failed_state = FailedState()

        print(f"Available states: {type(pending_state).__name__}, {type(success_state).__name__}, {type(failed_state).__name__}")
        print("State pattern allows transactions to change behavior based on their current state")
        print("- PendingState: Can process or cancel")
        print("- SuccessState: Can refund")
        print("- FailedState: Can cancel or refund")

    def demo_chain_processing(self):
        print("\n=== Chain Processing Demo ===")

        chain = PaymentChainFactory.create_full_chain()
        print("Payment processing chain created with:")
        print("- Validation Handler")
        print("- Authentication Handler")
        print("- Fraud Handler")
        print("- Routing Handler")
        print("- Settlement Handler")

    def demo_observers(self):
        print("\n=== Observers Demo ===")

        # Create concrete observers
        payment_observer = ConcretePaymentObserver()
        transaction_observer = ConcreteTransactionObserver()

        # Create a payment and add observers
        payer_account = self.upi_app.account_repository.get_account_by_vpa(self.amit_vpa)
        payee_account = self.upi_app.account_repository.get_account_by_vpa(self.rahul_vpa)
        payment = Payment(PaymentType.DEBIT, PaymentMethod.UPI_PUSH, 300.0, payer_account, payee_account, Currency.INR)

        # Add observers to payment
        payment.add_observer(payment_observer)
        payment.add_observer(transaction_observer)

        print(f"Added {len(payment.observers)} observers to payment")

        # Simulate payment status change to trigger observers
        payment.set_status(PaymentStatus.APPROVED)
        print("Payment status changed to APPROVED - observers notified")

        # Cancel the payment to stop the timer
        payment.cancel_payment()

    def demo_proxies_and_decorators(self):
        print("\n=== Proxies & Decorators Demo ===")

        print("Rate limiting proxy active")
        print("Fraud check decorator active")
        print("Secure bank proxy active")

        response = self.upi_app.send_money(self.priya_vpa, self.amit_vpa, 2500.0)
        print(f"Protected transaction result: {response.status}")

    def demo_exception_handling(self):
        print("\n=== Exception Handling Demo ===")

        try:
            # Try to withdraw more than available balance
            account = self.upi_app.account_repository.get_account_by_vpa(self.rahul_vpa)
            print(f"Current balance: ₹{account.get_balance()}")

            # This should trigger InsufficientFundsException
            account.withdraw(50000.0)  # More than available balance

        except InsufficientFundsException as e:
            print(f"Exception caught: {e}")
            print("Exception handling pattern working correctly!")

    def demo_account_observer(self):
        print("\n=== Account Observer Demo ===")

        # Create account observer
        account_observer = ConcreteAccountObserver()

        # Get account and add observer
        account = self.upi_app.account_repository.get_account_by_vpa(self.rahul_vpa)
        account.add_observer(account_observer)

        print(f"Initial balance: ₹{account.get_balance()}")

        # Simulate balance change to trigger observer
        account.deposit(1000.0)
        print("Account balance changed - observer notified")

    def demo_upi_adapter(self):
        print("\n=== UPI Adapter Demo ===")

        # Create UPI adapter
        upi_adapter = UPIAdapter()

        # Test UPI payment processing
        request_data = {"payer_vpa": self.rahul_vpa, "payee_vpa": self.priya_vpa, "amount": 500.0}

        print("Processing payment through UPI Adapter...")
        response = upi_adapter.process_payment(request_data)
        print(f"UPI Adapter response: {response.status}")

        # Test balance check
        balance_response = upi_adapter.check_balance(self.rahul_vpa)
        print(f"Balance check result: ₹{balance_response.amount}")

    def run_complete_demo(self):
        print("=" * 60)
        print("UPI PAYMENT SYSTEM COMPREHENSIVE DEMO")
        print("=" * 60)

        self.demo_cross_bank_transfer()
        self.demo_money_request()
        self.demo_credit_card_payment()
        self.demo_fraud_detection()
        self.demo_transaction_states()
        self.demo_chain_processing()
        self.demo_observers()
        self.demo_proxies_and_decorators()
        self.demo_exception_handling()
        self.demo_account_observer()
        self.demo_upi_adapter()

        print("\n" + "=" * 60)
        print("DEMO COMPLETED - ALL PATTERNS DEMONSTRATED")
        print("=" * 60)

        print("\nDesign Patterns Showcased:")
        print("✓ Abstract Factory - Bank integration")
        print("✓ Adapter - Bank & UPI communication")
        print("✓ Chain of Responsibility - Payment processing")
        print("✓ Command - Payment operations")
        print("✓ Decorator - Fraud detection")
        print("✓ Exception Handling - Error management")
        print("✓ Observer - Payment, Transaction & Account notifications")
        print("✓ Proxy - Access control & rate limiting")
        print("✓ Repository - Data access layer")
        print("✓ Service - Business logic layer")
        print("✓ Strategy - Payment methods")
        print("✓ State - Transaction lifecycle")
        print("✓ Facade - UPIApp interface")
        print("✓ Model - Domain entities")


if __name__ == "__main__":
    demo = UPIDemo()
    demo.run_complete_demo()
