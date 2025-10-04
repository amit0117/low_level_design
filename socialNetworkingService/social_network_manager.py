from app.services.user_service import UserService
from app.services.post_service import PostService
from app.services.feed_service import FeedService
from threading import Lock
from app.models.user import User
from app.models.post import Post
from app.models.connection import Connection
from app.models.notification import Notification
from app.models.comment import Comment
from app.models.like import Like


class SocialNetworkManager:
    _instance: "SocialNetworkManager" = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "has_initialized"):
            return
        self.user_service = UserService()
        self.post_service = PostService()
        self.feed_service = FeedService()
        self.has_initialized = True

    @classmethod
    def get_instance(cls) -> "SocialNetworkManager":
        return cls()

    def register_user(self, name: str, email: str, password: str, username: str) -> User:
        return self.user_service.register_user(name, email, password, username)

    def login_user(self, username: str, password: str) -> User:
        return self.user_service.login_user(username, password)

    def send_friend_request(self, user_id: str, friend_id: str) -> Connection:
        return self.user_service.send_connection_request(user_id, friend_id)

    def accept_friend_request(self, connection: Connection, to_user_id: str) -> None:
        self.user_service.accept_connection_request(connection, to_user_id)

    def reject_friend_request(self, connection: Connection, to_user_id: str) -> None:
        self.user_service.reject_connection_request(connection, to_user_id)

    def withdraw_friend_request(self, connection: Connection, to_user_id: str) -> None:
        self.user_service.withdraw_connection_request(connection, to_user_id)

    def get_all_connections(self, user_id: str) -> list[Connection]:
        return self.user_service.get_all_connections(user_id)

    def get_all_notifications(self, user_id: str) -> list[Notification]:
        return self.user_service.get_all_notifications(user_id)

    def get_all_friends(self, user_id: str) -> list[User]:
        return self.user_service.get_all_friends(user_id)

    def create_post(self, user_id: str, content: str) -> Post:
        return self.post_service.create_post(user_id, content)

    def like_post(self, user_id: str, post_id: str) -> None:
        return self.post_service.like_post(user_id, post_id)

    def add_comment(self, user_id: str, post_id: str, content: str) -> None:
        return self.post_service.add_comment(user_id, post_id, content)

    def get_all_posts(self) -> list[Post]:
        return self.post_service.get_all_posts()

    def get_all_posts_by_user_id(self, user_id: str) -> list[Post]:
        return self.post_service.get_all_posts_by_user_id(user_id)

    def get_all_comments(self, post_id: str) -> list[Comment]:
        return self.post_service.get_all_comments(post_id)

    def get_all_likes(self, post_id: str) -> list[Like]:
        return self.post_service.get_all_likes(post_id)
