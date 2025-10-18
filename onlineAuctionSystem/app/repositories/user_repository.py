from app.models.user import User
from threading import Lock


class UserRepository:
    _instance: "UserRepository" = None
    _lock: Lock = Lock()

    def __new__(cls) -> "UserRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "users"):
            return
        self.users: dict[str, User] = dict()

    @classmethod
    def get_instance(cls) -> "UserRepository":
        return cls._instance or cls()

    def add_user(self, user: User):
        with self._lock:
            self.users[user.get_id()] = user

    def get_user(self, id: str) -> User:
        return self.users.get(id)

    def get_all_users(self) -> list[User]:
        return list(self.users.values())

    def remove_user(self, id: str) -> None:
        with self._lock:
            self.users.pop(id, None)

    def get_user_by_email(self, email: str) -> User:
        return next((user for user in self.users.values() if user.get_email() == email), None)

    def get_user_by_id(self, id: str) -> User:
        return self.users.get(id)

    def get_user_by_name(self, name: str) -> User:
        return next((user for user in self.users.values() if user.get_name() == name), None)
