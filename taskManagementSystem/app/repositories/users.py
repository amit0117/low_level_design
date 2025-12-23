from typing import Optional, TYPE_CHECKING
from threading import Lock

if TYPE_CHECKING:
    from app.models.user import User


class UserRepository:
    _instance: Optional["UserRepository"] = None
    _lock = Lock()

    def __new__(cls) -> "UserRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "users"):
            return
        self.process_lock = Lock()
        self.users: dict[str, "User"] = dict()

    @classmethod
    def get_instance(cls) -> "UserRepository":
        return cls._instance or cls()

    def add_user(self, user: "User") -> None:
        with self.process_lock:
            self.users[user.get_id()] = user

    def remove_user(self, user: "User") -> None:
        with self.process_lock:
            if user.get_id() not in self.users:
                raise ValueError("User not found")
            del self.users[user.get_id()]

    def get_user_by_id(self, user_id: str) -> Optional["User"]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional["User"]:
        return next((user for user in self.users.values() if user.get_email() == email), None)

    def get_user_by_name(self, name: str) -> Optional["User"]:
        return next((user for user in self.users.values() if user.get_name() == name), None)

    def get_all_users(self) -> list["User"]:
        return list(self.users.values())

    def update_user(self, user: "User") -> None:
        with self.process_lock:
            if user.get_id() not in self.users:
                raise ValueError("User not found")
            self.users[user.get_id()] = user
