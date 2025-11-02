from app.models.atm import ATM
from app.models.account import Account
from app.models.card import Card
from app.repositories.bank_repository import BankRepository
from app.exceptions.insufficient_money import InsufficientFundsException, InsufficientCashException


class TransactionService:
    """
    Service layer to handle all types of ATM transactions
    Coordinates between ATM, accounts, cards, and banks
    Provides a clean interface for transaction operations
    """

    def __init__(self, atm: ATM):
        self.atm = atm
        self.bank_repository = BankRepository.get_instance()

    def balance_inquiry(self, account: Account, card: Card, pin: str) -> float:
        """
        Perform balance inquiry transaction

        Args:
            account: Account to check balance
            card: Card associated with the account
            pin: PIN for authentication

        Returns:
            Current account balance

        Raises:
            ValueError: If card/PIN validation fails
        """
        try:
            bank_name = account.get_bank_name()
            print(f"\n=== Balance Inquiry ===")
            print(f"Account: {account.get_account_number()}")
            print(f"Bank: {bank_name}")

            self.atm.check_balance(bank_name, account, card, pin)

            # Get balance from bank server
            bank_server = self.bank_repository.get_bank_server(bank_name)
            balance = bank_server.get_account_balance(account.get_account_number())
            print(f"Current Balance: {balance}")
            return balance

        except Exception as e:
            print(f"Balance inquiry failed: {e}")
            raise

    def debit(self, account: Account, card: Card, pin: str, amount: float) -> bool:
        """
        Perform debit (withdrawal) transaction

        Args:
            account: Account to debit from
            card: Card associated with the account
            pin: PIN for authentication
            amount: Amount to withdraw

        Returns:
            True if successful, False otherwise

        Raises:
            InsufficientFundsException: If account has insufficient funds
            InsufficientCashException: If ATM has insufficient cash
            ValueError: If validation fails
        """
        try:
            bank_name = account.get_bank_name()
            print(f"\n=== Withdrawal Transaction ===")
            print(f"Account: {account.get_account_number()}")
            print(f"Bank: {bank_name}")
            print(f"Amount: {amount}")

            # Check cash availability in ATM
            if not self.atm.cash_dispenser.has_sufficient_cash(int(amount)):
                raise InsufficientCashException(f"ATM has insufficient cash. Available: {self.atm.cash_dispenser.get_cash_available()}")

            # Check account balance
            bank_server = self.bank_repository.get_bank_server(bank_name)
            current_balance = bank_server.get_account_balance(account.get_account_number())
            if current_balance < amount:
                raise InsufficientFundsException(f"Insufficient funds in account. Available: {current_balance}")

            # Perform withdrawal
            self.atm.withdraw(bank_name, account, amount, card, pin)

            # Get updated balance
            new_balance = bank_server.get_account_balance(account.get_account_number())
            print(f"Withdrawal successful!")
            print(f"Previous Balance: {current_balance}")
            print(f"New Balance: {new_balance}")
            print(f"Cash dispensed: {amount}")
            return True

        except (InsufficientFundsException, InsufficientCashException) as e:
            print(f"Withdrawal failed: {e}")
            raise
        except Exception as e:
            print(f"Withdrawal failed: {e}")
            raise

    def credit(self, account: Account, card: Card, pin: str, amount: float) -> bool:
        """
        Perform credit (deposit) transaction

        Args:
            account: Account to credit to
            card: Card associated with the account
            pin: PIN for authentication
            amount: Amount to deposit

        Returns:
            True if successful, False otherwise

        Raises:
            ValueError: If validation fails
        """
        try:
            bank_name = account.get_bank_name()
            print(f"\n=== Deposit Transaction ===")
            print(f"Account: {account.get_account_number()}")
            print(f"Bank: {bank_name}")
            print(f"Amount: {amount}")

            # Get current balance
            bank_server = self.bank_repository.get_bank_server(bank_name)
            current_balance = bank_server.get_account_balance(account.get_account_number())

            # Perform deposit
            self.atm.deposit(bank_name, account, amount, card, pin)

            # Get updated balance
            new_balance = bank_server.get_account_balance(account.get_account_number())
            print(f"Deposit successful!")
            print(f"Previous Balance: {current_balance}")
            print(f"New Balance: {new_balance}")
            print(f"Amount deposited: {amount}")
            return True

        except Exception as e:
            print(f"Deposit failed: {e}")
            raise

    def transfer(self, source_account: Account, destination_account: Account, card: Card, pin: str, amount: float) -> bool:
        """
        Perform transfer transaction between accounts

        Args:
            source_account: Account to transfer from
            destination_account: Account to transfer to
            card: Card associated with source account
            pin: PIN for authentication
            amount: Amount to transfer

        Returns:
            True if successful, False otherwise

        Raises:
            InsufficientFundsException: If source account has insufficient funds
            ValueError: If validation fails
        """
        try:
            source_bank_name = source_account.get_bank_name()
            destination_bank_name = destination_account.get_bank_name()

            print(f"\n=== Transfer Transaction ===")
            print(f"Source Account: {source_account.get_account_number()} ({source_bank_name})")
            print(f"Destination Account: {destination_account.get_account_number()} ({destination_bank_name})")
            print(f"Amount: {amount}")

            # Check source account balance
            source_bank_server = self.bank_repository.get_bank_server(source_bank_name)
            source_balance = source_bank_server.get_account_balance(source_account.get_account_number())
            if source_balance < amount:
                raise InsufficientFundsException(f"Insufficient funds in source account. Available: {source_balance}")

            # Get destination balance
            destination_bank_server = self.bank_repository.get_bank_server(destination_bank_name)
            destination_balance = destination_bank_server.get_account_balance(destination_account.get_account_number())

            # Perform transfer
            self.atm.transfer(source_bank_name, destination_bank_name, source_account, destination_account, amount, card, pin)

            # Get updated balances
            new_source_balance = source_bank_server.get_account_balance(source_account.get_account_number())
            new_destination_balance = destination_bank_server.get_account_balance(destination_account.get_account_number())

            print(f"Transfer successful!")
            print(f"Source Account:")
            print(f"  Previous Balance: {source_balance}")
            print(f"  New Balance: {new_source_balance}")
            print(f"Destination Account:")
            print(f"  Previous Balance: {destination_balance}")
            print(f"  New Balance: {new_destination_balance}")
            return True

        except InsufficientFundsException as e:
            print(f"Transfer failed: {e}")
            raise
        except Exception as e:
            print(f"Transfer failed: {e}")
            raise

    def get_account_info(self, account: Account) -> dict:
        """
        Get account information

        Args:
            account: Account to get info for

        Returns:
            Dictionary with account information
        """
        bank_server = self.bank_repository.get_bank_server(account.get_bank_name())
        balance = bank_server.get_account_balance(account.get_account_number())

        return {
            "account_number": account.get_account_number(),
            "account_type": account.get_account_type().value,
            "bank_name": account.get_bank_name(),
            "balance": balance,
            "user_name": account.get_user().get_name(),
        }

    def get_atm_status(self) -> dict:
        """
        Get ATM status and information

        Returns:
            Dictionary with ATM status information
        """
        return {
            "atm_id": self.atm.get_id(),
            "atm_name": self.atm.get_name(),
            "status": self.atm.get_status().value,
            "cash_available": self.atm.cash_dispenser.get_cash_available(),
            "low_cash_threshold": self.atm.cash_dispenser.low_cash_threshold,
        }
