from app.models.user import User
from typing import Optional
from threading import Lock


class UserRepository:
    _instance: Optional["UserRepository"] = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "users"):
            return
        self.process_lock = Lock()
        self.users: list[User] = []

    @classmethod
    def get_instance(cls) -> "UserRepository":
        return cls()

    def add_user(self, user: User) -> None:
        with self.process_lock:
            self.users.append(user)

    def remove_user(self, user: User) -> None:
        with self.process_lock:
            if user not in self.users:
                raise ValueError("User not found")
            self.users.remove(user)

    def get_user(self, id: str) -> User:
        return self.users[id]

    def get_all_users(self) -> list[User]:
        return self.users

    def get_user_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self.users if user.get_email().lower() == email.lower()), None)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return next((user for user in self.users if user.get_username().lower() == username.lower()), None)

    def get_user_by_id(self, id: str) -> Optional[User]:
        return next((user for user in self.users if user.get_id() == id), None)
