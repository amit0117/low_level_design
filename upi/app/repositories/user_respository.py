from app.models.user import User
from threading import Lock
from typing import Optional


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
        self.users: dict[str, User] = {}

    @classmethod
    def get_instance(cls) -> "UserRepository":
        return cls._instance or cls()

    def add_user(self, user: User) -> None:
        self.users[user.get_id()] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def update_user(self, user: User) -> None:
        self.users[user.get_id()] = user

    def delete_user(self, user_id: str) -> None:
        self.users.pop(user_id, None)

    def get_all_users(self) -> list[User]:
        return list(self.users.values())
