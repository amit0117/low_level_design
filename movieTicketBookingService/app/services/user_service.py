from app.models.user import User


class UserService:
    def __init__(self):
        self.users: dict[str, User] = {}

    def register_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise ValueError(f"User with id {user_id} not found")
        return self.users[user_id]

    def get_all_users(self) -> list[User]:
        return list(self.users.values())
