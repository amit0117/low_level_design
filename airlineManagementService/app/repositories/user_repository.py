from app.models.user import User
from typing import Optional
from threading import Lock
from app.models.enums import UserType
from app.models.user import Passenger
from app.models.user import Staff
from app.models.user import Admin
from app.models.enums import StaffType


class UserRepository:
    _instance: Optional["UserRepository"] = None
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
        self.users: dict[str, User] = {}

    @classmethod
    def get_instance(cls: type["UserRepository"]) -> "UserRepository":
        return cls._instance or cls()

    def add_user(self, user: User):
        self.users[user.get_id()] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def update_user(self, user_id: str, user: User):
        self.users[user_id] = user

    def delete_user(self, user_id: str):
        del self.users[user_id]

    def get_all_users(self) -> list[User]:
        return list(self.users.values())

    def get_all_users_by_type(self, user_type: UserType) -> list[User]:
        return [user for user in self.users.values() if user.get_user_type() == user_type]

    def get_all_passengers(self) -> list[Passenger]:
        return self.get_all_users_by_type(UserType.PASSENGER)

    def get_all_airline_staff(self) -> list[Staff]:
        return self.get_all_users_by_type(UserType.AIRLINE_STAFF)

    def get_all_admins(self) -> list[Admin]:
        return self.get_all_users_by_type(UserType.ADMIN)

    def get_all_cabin_crew(self) -> list[Staff]:
        return [staff for staff in self.get_all_airline_staff() if staff.get_staff_type() == StaffType.CABIN_CREW]

    def get_all_cockpit_crew(self) -> list[Staff]:
        return [staff for staff in self.get_all_airline_staff() if staff.get_staff_type() == StaffType.COCKPIT_CREW]
