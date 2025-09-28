from app.services.user_service import UserService
from app.services.group_service import GroupService
from app.models.user import User
from app.models.group import Group
import threading
from app.models.expense import Expense
from app.models.balance_sheet import BalanceSheet


class SplitWiseService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SplitWiseService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_has_initialized"):
            return
        self.user_service = UserService()
        self.group_service = GroupService()
        self._has_initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    def add_user(self, name: str, email: str) -> User:
        return self.user_service.create_user(name, email)

    def add_group(self, name: str, members: list[User]) -> Group:
        return self.group_service.create_group(name, members)

    def get_user(self, user_id: str) -> User:
        return self.user_service.get_user(user_id)

    def get_group(self, group_id: str) -> Group:
        return self.group_service.get_group(group_id)

    def add_expense_to_group(self, group_id: str, expense: Expense) -> None:
        self.group_service.add_expense(group_id, expense)

    def show_user_balance_sheet(self, user_id: str) -> None:
        self.user_service.show_balance_sheet(user_id)

    def settle_up(self, user_id1: str, user_id2: str, amount: float) -> None:
        self.user_service.settle_up(user_id1, user_id2, amount)
