from typing import Optional, List
from app.models.user import User
from app.models.enums import UserType
from app.models.address import Address


class UserService:
    """Service for managing users"""

    def __init__(self):
        self.users: dict[str, User] = {}

    def add_user(self, user: User):
        """Add a new user"""
        if user.get_user_id() in self.users:
            print(f"User with id {user.get_user_id()} already exists. Try logging in instead.")
            return
        self.users[user.get_user_id()] = user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        if user_id not in self.users:
            print(f"User with id {user_id} not found. Try registering instead.")
            return None
        return self.users.get(user_id)

    def get_user_by_name(self, user_name: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users.values():
            if user.get_user_name() == user_name:
                return user
        return None

    def authenticate_user(self, user_name: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_user_by_name(user_name)
        if user and user.get_account().verify_password(password):
            return user
        return None

    def update_user_address(self, user_id: str, new_address: Address) -> bool:
        """Update user's shipping address"""
        user = self.get_user(user_id)
        if user:
            user.set_address(new_address)
            return True
        return False

    def get_all_users(self) -> List[User]:
        """Get all users"""
        return list(self.users.values())

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
