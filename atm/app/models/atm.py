from app.models.card_reader import CardReader
from app.models.keypad import Keypad
from app.models.cash_dispenser import CashDispenser
from app.models.bank_server import BankServer
from app.models.card import Card
from app.models.user import User
from app.models.account import Account
from uuid import uuid4
from app.models.enums import TransactionType, ATMStatus
from app.factories.transaction_factory import (
    WithdrawalTransactionFactory,
    DepositTransactionFactory,
    TransferTransactionFactory,
    BalanceInquiryTransactionFactory,
)
from app.states.idle_state import IdleState
from app.states.card_inserted_state import CardInsertedState
from app.states.authenticated_state import AuthenticatedState
from app.states.transaction_selected_state import TransactionSelectedState
from app.states.transaction_processing_state import TransactionProcessingState
from app.states.out_of_service_state import OutOfServiceState
from typing import Optional


class ATM:
    def __init__(self, name: str, bank_server: BankServer, card_reader: CardReader, keypad: Keypad, cash_dispenser: CashDispenser):
        self.id = str(uuid4())
        self.name = name
        self.bank_server = bank_server
        self.card_reader = card_reader
        self.keypad = keypad
        self.cash_dispenser = cash_dispenser
        self.status = ATMStatus.IDLE

        # State pattern initialization
        self.idle_state = IdleState()
        self.card_inserted_state = CardInsertedState()
        self.authenticated_state = AuthenticatedState()
        self.transaction_selected_state = TransactionSelectedState()
        self.transaction_processing_state = TransactionProcessingState()
        self.out_of_service_state = OutOfServiceState()
        self.current_state = self.idle_state

        # Transaction context
        self.current_card: Optional[Card] = None
        self.current_pin: Optional[str] = None
        self.current_account: Optional[Account] = None
        self.current_transaction_type: Optional[TransactionType] = None

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def change_bank_server(self, bank_server: BankServer) -> None:
        self.bank_server = bank_server

    def list_available_transactions_options(self) -> None:
        print("Available transactions : \n")
        for txn_type in TransactionType:
            print(f"{txn_type.value}: {txn_type.name}")
        print("\n")

    def change_state(self, new_state) -> None:
        """Change the current state of the ATM"""
        self.current_state = new_state

    def insert_card(self, card: Card) -> None:
        """Insert card - delegated to current state"""
        self.current_state.insert_card(self, card)

    def eject_card(self) -> None:
        """Eject card - delegated to current state"""
        self.current_state.eject_card(self)

    def enter_pin(self) -> None:
        """Enter PIN - delegated to current state, which uses keypad to read PIN"""
        self.current_state.enter_pin(self)

    def select_transaction(self, txn_type: TransactionType) -> None:
        """Select transaction type - delegated to current state"""
        self.current_state.select_transaction(self, txn_type)

    def perform_transaction(self, amount: Optional[float] = None) -> None:
        """Perform transaction - delegated to current state"""
        self.current_state.perform_transaction(self, amount)

    def withdraw(self, bank_name: str, account: Account, amount: float, card: Card, pin: str) -> None:
        """Withdraw money using Transaction Factory + Template Method pattern"""
        txn = WithdrawalTransactionFactory().create_transaction(bank_name, account, amount, self.cash_dispenser, card, pin)
        txn.execute()

    def deposit(self, bank_name: str, account: Account, amount: float, card: Card, pin: str) -> None:
        """Deposit money using Transaction Factory + Template Method pattern"""
        txn = DepositTransactionFactory().create_transaction(bank_name, account, amount, card, pin)
        txn.execute()

    def transfer(
        self,
        source_bank_name: str,
        destination_bank_name: str,
        source_account: Account,
        destination_account: Account,
        amount: float,
        card: Card,
        pin: str,
    ) -> None:
        """Transfer money using Transaction Factory + Template Method pattern"""
        txn = TransferTransactionFactory().create_transaction(
            source_bank_name, destination_bank_name, source_account, destination_account, amount, card, pin
        )
        txn.execute()

    def check_balance(self, bank_name: str, account: Account, card: Card, pin: str) -> None:
        txn = BalanceInquiryTransactionFactory().create_transaction(bank_name, account, card, pin)
        txn.execute()

    def get_status(self) -> ATMStatus:
        return self.status

    def set_status(self, status: ATMStatus) -> None:
        self.status = status

    def set_out_of_service(self) -> None:
        self.change_state(self.out_of_service_state)
        self.set_status(ATMStatus.OUT_OF_SERVICE)

    def set_back_to_service(self) -> None:
        self.change_state(self.idle_state)
        self.set_status(ATMStatus.IDLE)
