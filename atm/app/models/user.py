from app.models.account import Account
from app.models.enums import UserType
from app.observers.base_observer import BaseObserver
from app.models.card import Card
from threading import Lock


class User(BaseObserver):
    def __init__(self, name: str, user_type: UserType, accounts: list[Account] = None, cards: list[Card] = None):
        super().__init__()
        self.name = name
        self.user_type = user_type
        self.accounts: list[Account] = accounts or []
        self.cards: list[Card] = cards or []
        self.lock = Lock()

    def get_name(self) -> str:
        return self.name

    def get_accounts(self) -> list[Account]:
        with self.lock:
            return self.accounts.copy()

    def get_cards(self) -> list[Card]:
        with self.lock:
            return self.cards.copy()

    def get_user_type(self) -> UserType:
        return self.user_type

    def update(self, message: str) -> None:
        print(f"Update for user {self.name} \n Message: {message}\n\n")

    def add_account(self, account: Account) -> None:
        with self.lock:
            self.accounts.append(account)

    def add_card(self, card: Card) -> None:
        with self.lock:
            self.cards.append(card)

    def remove_account(self, account: Account) -> None:
        with self.lock:
            if account not in self.accounts:
                raise ValueError(f"Account {account.get_account_number()} not found in user {self.name}'s accounts")
            self.accounts.remove(account)

    def remove_card(self, card: Card) -> None:
        with self.lock:
            if card not in self.cards:
                raise ValueError(f"Card {card.get_card_number()} not found in user {self.name}'s cards")
            self.cards.remove(card)


class Admin(User):
    def __init__(self, name: str, account: Account):
        super().__init__(name, account, UserType.ADMIN)

    def update(self, message: str) -> None:
        print(f"Update for admin {self.name} \n Message: {message}\n\n")


class Customer(User):
    def __init__(self, name: str, account: Account):
        super().__init__(name, account, UserType.CUSTOMER)

    def update(self, message: str) -> None:
        print(f"Update for customer {self.name} \n Message: {message}\n\n")
