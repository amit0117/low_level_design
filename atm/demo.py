"""
ATM System Demo
Demonstrates all transaction types and various test scenarios
"""

import threading
from atm_machine import ATMMachine
from app.models.enums import AccountType, TransactionType


def print_separator(title: str):
    """Print a separator with title"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_balance_inquiry(atm: ATMMachine, card_number: str, pin: str):
    """Test balance inquiry transaction"""
    print("📊 Testing Balance Inquiry...")
    balance = atm.balance_inquiry(card_number, pin)
    if balance is not None:
        print(f"✅ Balance inquiry successful. Current balance: ₹{balance:,.2f}\n")
    else:
        print("❌ Balance inquiry failed\n")


def test_withdrawal(atm: ATMMachine, card_number: str, pin: str, amount: float):
    """Test withdrawal transaction"""
    print(f"💸 Testing Withdrawal of ₹{amount:,.2f}...")
    result = atm.withdraw(card_number, pin, amount)
    if result:
        print(f"✅ Withdrawal successful\n")
    else:
        print(f"❌ Withdrawal failed\n")


def test_deposit(atm: ATMMachine, card_number: str, pin: str, amount: float):
    """Test deposit transaction"""
    print(f"💰 Testing Deposit of ₹{amount:,.2f}...")
    result = atm.deposit(card_number, pin, amount)
    if result:
        print(f"✅ Deposit successful\n")
    else:
        print(f"❌ Deposit failed\n")


def test_transfer(atm: ATMMachine, source_card: str, pin: str, dest_account: str, amount: float):
    """Test transfer transaction"""
    print(f"🔄 Testing Transfer of ₹{amount:,.2f}...")
    result = atm.transfer(source_card, pin, dest_account, amount)
    if result:
        print(f"✅ Transfer successful\n")
    else:
        print(f"❌ Transfer failed\n")


def test_inter_bank_transfer(atm: ATMMachine):
    """Test inter-bank transfer (HDFC to SBI)"""
    print_separator("Test 1: Inter-Bank Transfer (HDFC → SBI)")

    # HDFC user transfers to SBI user
    source_card = "CARD001"  # Rahul's HDFC card
    destination_account = "ACC002"  # Priya's SBI account

    print(f"Source: Card {source_card} (HDFC)")
    print(f"Destination: Account {destination_account} (SBI)")

    # Show balances before
    print("\nBefore Transfer:")
    atm.balance_inquiry(source_card, "1234")
    if destination_account in atm.accounts:
        account = atm.accounts[destination_account]
        balance_info = atm.transaction_service.get_account_info(account)
        print(f"Destination Account Balance: ₹{balance_info['balance']:,.2f}")

    # Perform transfer
    test_transfer(atm, source_card, "1234", destination_account, 5000.0)

    # Show balances after
    print("After Transfer:")
    atm.balance_inquiry(source_card, "1234")
    if destination_account in atm.accounts:
        account = atm.accounts[destination_account]
        balance_info = atm.transaction_service.get_account_info(account)
        print(f"Destination Account Balance: ₹{balance_info['balance']:,.2f}")


def test_multiple_simultaneous_transactions(atm: ATMMachine):
    """Test multiple simultaneous transactions on same account"""
    print_separator("Test 2: Multiple Simultaneous Transactions on Same Account")

    card_number = "CARD001"
    pin = "1234"
    account_number = "ACC001"

    def concurrent_transaction(transaction_type: str, amount: float):
        """Helper function for concurrent transactions"""
        print(f"Thread {threading.current_thread().name}: Starting {transaction_type}")
        try:
            if transaction_type == TransactionType.WITHDRAWAL:
                atm.withdraw(card_number, pin, amount)
            elif transaction_type == TransactionType.DEPOSIT:
                atm.deposit(card_number, pin, amount)
            elif transaction_type == TransactionType.BALANCE_INQUIRY:
                atm.balance_inquiry(card_number, pin)
            print(f"Thread {threading.current_thread().name}: {transaction_type} completed")
        except Exception as e:
            print(f"Thread {threading.current_thread().name}: {transaction_type} failed - {e}")

    print("Initial Balance:")
    atm.balance_inquiry(card_number, pin)

    print("\nStarting 5 concurrent transactions...")
    threads: list[threading.Thread] = []

    # Create multiple threads for different transactions
    threads.append(threading.Thread(target=concurrent_transaction, args=(TransactionType.WITHDRAWAL, 2000), name="Thread-Withdraw-1"))
    threads.append(threading.Thread(target=concurrent_transaction, args=(TransactionType.WITHDRAWAL, 1500), name="Thread-Withdraw-2"))
    threads.append(threading.Thread(target=concurrent_transaction, args=(TransactionType.DEPOSIT, 3000), name="Thread-Deposit-1"))
    threads.append(threading.Thread(target=concurrent_transaction, args=(TransactionType.BALANCE_INQUIRY, 0), name="Thread-Balance-1"))
    threads.append(threading.Thread(target=concurrent_transaction, args=(TransactionType.BALANCE_INQUIRY, 0), name="Thread-Balance-2"))

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\nFinal Balance:")
    atm.balance_inquiry(card_number, pin)


def test_insufficient_funds_transfer(atm: ATMMachine):
    """Test transfer when source account has insufficient funds"""
    print_separator("Test 3: Transfer with Insufficient Funds")

    source_card = "CARD001"  # Rahul's card
    pin = "1234"
    destination_account = "ACC002"  # Priya's account

    print("Checking source account balance...")
    balance = atm.balance_inquiry(source_card, pin)

    if balance is not None:
        transfer_amount = balance + 10000  # Transfer more than available
        print(f"\nAttempting to transfer ₹{transfer_amount:,.2f} (Available: ₹{balance:,.2f})")
        test_transfer(atm, source_card, pin, destination_account, transfer_amount)
    else:
        print("❌ Could not check balance")


def test_insufficient_cash_in_atm(atm: ATMMachine):
    """Test withdrawal when ATM has insufficient cash"""
    print_separator("Test 4: Withdrawal with Insufficient Cash in ATM")

    card_number = "CARD001"
    pin = "1234"

    print("Checking ATM cash availability...")
    status = atm.get_atm_status()
    print(f"ATM Cash Available: ₹{status['cash_available']:,.2f}")

    # Check account balance
    balance = atm.balance_inquiry(card_number, pin)

    if balance is not None:
        # Try to withdraw more than ATM has
        withdrawal_amount = status["cash_available"] + 5000
        print(f"\nAttempting to withdraw ₹{withdrawal_amount:,.2f}")
        print(f"ATM has only ₹{status['cash_available']:,.2f}")
        test_withdrawal(atm, card_number, pin, withdrawal_amount)
    else:
        print("❌ Could not check balance")


def main():
    """Main demo function"""
    print_separator("🏧 ATM System Demo - Initialization")

    # Initialize ATM Machine
    atm = ATMMachine("Main ATM", initial_cash=50000.0)

    # Add users from different banks
    print_separator("👥 Setting Up Users")

    # HDFC Bank Users
    atm.add_user("Rahul", "HDFC", "ACC001", AccountType.SAVINGS, 50000.0, "1234", "CARD001")
    atm.add_user("Amit", "HDFC", "ACC003", AccountType.SAVINGS, 30000.0, "5678", "CARD003")

    # SBI Bank Users
    atm.add_user("Priya", "SBI", "ACC002", AccountType.SAVINGS, 40000.0, "5678", "CARD002")
    atm.add_user("Sneha", "SBI", "ACC004", AccountType.SAVINGS, 25000.0, "9012", "CARD004")

    # ICICI Bank Users
    atm.add_user("Raj", "ICICI", "ACC005", AccountType.SAVINGS, 35000.0, "3456", "CARD005")

    # Add Admin
    atm.add_admin("Admin", "HDFC", "ADMIN001", AccountType.SAVINGS, 100000.0)

    # Display all users
    atm.display_all_users()

    # Display ATM info
    atm.display_atm_info()

    # Test 1: Basic Transaction Types
    print_separator("Basic Transaction Types")

    print("1️⃣ Balance Inquiry")
    test_balance_inquiry(atm, "CARD001", "1234")

    print("2️⃣ Withdrawal")
    test_withdrawal(atm, "CARD001", "1234", 5000.0)
    test_balance_inquiry(atm, "CARD001", "1234")

    print("3️⃣ Deposit")
    test_deposit(atm, "CARD001", "1234", 2000.0)
    test_balance_inquiry(atm, "CARD001", "1234")

    print("4️⃣ Transfer (Same Bank)")
    test_transfer(atm, "CARD001", "1234", "ACC003", 3000.0)
    test_balance_inquiry(atm, "CARD001", "1234")

    # Test 2: Inter-Bank Transfer
    test_inter_bank_transfer(atm)

    # Test 3: Multiple Simultaneous Transactions
    test_multiple_simultaneous_transactions(atm)

    # Test 4: Insufficient Funds Transfer
    test_insufficient_funds_transfer(atm)

    # Test 5: Insufficient Cash in ATM
    test_insufficient_cash_in_atm(atm)

    # Final Status
    print_separator("Final ATM Status")
    atm.display_atm_info()
    atm.display_all_users()

    print_separator("✅ Demo Completed Successfully")


if __name__ == "__main__":
    main()
