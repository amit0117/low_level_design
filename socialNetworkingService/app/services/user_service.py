from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.connection import Connection
from app.models.notification import Notification
from app.exceptions.permission import PermissionError


class UserService:
    def __init__(self):
        self.user_repository = UserRepository.get_instance()

    def get_user_by_id(self, user_id: str) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def register_user(self, name: str, email: str, password: str, username: str) -> User:
        user = User(name, email, password, username)
        self.user_repository.add_user(user)
        return user

    def login_user(self, username: str, password: str) -> bool:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return True

    # connection related methods
    def send_connection_request(self, user_id: str, friend_id: str) -> Connection:
        if user_id == friend_id:
            raise PermissionError("User cannot send connection request to themselves")
        user = self.user_repository.get_user_by_id(user_id)
        friend = self.user_repository.get_user_by_id(friend_id)
        # check if the user and friend exist
        if not user or not friend:
            raise ValueError("User or friend not found")
        # check if the connection already exists
        if next((friend for friend in user.get_friends() if friend.get_id() == friend_id), None):
            raise PermissionError(f"Connection already exists between the users {user.get_name()} and {friend.get_name()}")

        connection = Connection(user, friend)
        connection.send_request()
        return connection

    def accept_connection_request(self, connection: Connection, to_user_id: str) -> None:
        to_user = self.user_repository.get_user_by_id(to_user_id)
        if not to_user:
            raise ValueError("User not found")
        if connection.get_to_user().get_id() != to_user_id:
            raise ValueError(f"{to_user.get_name()} is not authorized to accept the connection request with {connection.get_from_user().get_name()}")
        connection.accept_request()
        return connection

    def reject_connection_request(self, connection: Connection, to_user_id: str) -> None:
        to_user = self.user_repository.get_user_by_id(to_user_id)
        if not to_user:
            raise ValueError("User not found")
        if connection.get_to_user().get_id() != to_user_id:
            raise PermissionError(
                f"{to_user.get_name()} is not authorized to reject the connection request with {connection.get_from_user().get_name()}"
            )
        connection.reject_request()
        return connection

    def withdraw_connection_request(self, connection: Connection, to_user_id: str) -> None:
        to_user = self.user_repository.get_user_by_id(to_user_id)
        if not to_user:
            raise ValueError("User not found")
        if connection.get_to_user().get_id() != to_user_id:
            raise PermissionError(
                f"{to_user.get_name()} is not authorized to withdraw the connection request with {connection.get_from_user().get_name()}"
            )
        connection.withdraw_request()
        return connection

    def get_all_connections(self, user_id: str) -> list[Connection]:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user.get_connections()

    def get_all_notifications(self, user_id: str) -> list[Notification]:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user.get_notifications()

    def get_all_friends(self, user_id: str) -> list[User]:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user.get_friends()
