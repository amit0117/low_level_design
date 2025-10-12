from app.models.account import Account
from app.observers.account_observer import AccountObserver
from app.observers.transaction_observer import TransactionObserver
from app.observers.payment_observer import PaymentObserver
from app.models.payment import Payment
from app.models.transaction import Transaction
from app.models.enums import PaymentType
from uuid import uuid4


class User(AccountObserver, TransactionObserver, PaymentObserver):
    def __init__(self, name: str, phone: str, email: str) -> None:
        super().__init__()
        self.id = str(uuid4())
        self.name = name
        self.phone = phone
        self.email = email
        self.accounts: list[Account] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_phone(self) -> str:
        return self.phone

    def get_email(self) -> str:
        return self.email

    def get_accounts(self) -> list[Account]:
        return self.accounts

    def add_account(self, account: Account) -> None:
        print(f"New Account {account.get_account_number()} added to user {self.name}")
        self.accounts.append(account)

    def get_all_transactions(self) -> dict[str, list[Transaction]]:
        return {account.get_account_number(): account.get_transactions() for account in self.accounts}

    def update_on_account_balance_change(self, account: Account, amount: float, payment_type: PaymentType) -> None:
        if payment_type == PaymentType.DEBIT:
            print(f"User {self.name} has debited {amount} from account {account.get_account_number()}")
        else:
            print(f"User {self.name} has credited {amount} to account {account.get_account_number()}")

    def update_on_transaction(self, transaction: Transaction) -> None:
        print(
            f"User {self.name} has received a notification for transaction with id: {transaction.get_transaction_id()}.\n Status changed to {transaction.get_transaction_status()}\n"
        )

    def update_on_payment(self, payment: Payment) -> None:
        # Payment update is only for the payer
        if payment.get_payer_account().get_user() != self:
            return
        print(
            f"User {self.name} has received a notification for payment with id: {payment.get_payment_id()}.\n Status changed to {payment.get_status()}\n"
        )
