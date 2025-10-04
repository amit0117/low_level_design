from uuid import uuid4
from typing import Optional, TYPE_CHECKING
from app.models.notification import Notification
from app.models.enums import ConnectionStatus, NotificationType
from app.observers.connection_observer import ConnectionObserver
from app.observers.commentable_observer import CommentableObserver


if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.comment import Comment
    from app.models.like import Like
    from app.models.connection import Connection
    from app.models.commentable import Commentable


class Profile:
    def __init__(self, name: str, email: str, about: Optional[str] = None):
        self.name = name
        self.email = email
        self.about = about if about is not None else ""

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_about(self) -> str:
        return self.about

    def set_about(self, about: str) -> None:
        self.about = about


class Account:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_username(self) -> str:
        return self.username

    def set_password(self, password: str) -> None:
        self.password = password

    def is_valid_password(self, password: str) -> bool:
        return self.password == password


class User(ConnectionObserver, CommentableObserver):
    def __init__(self, name: str, email: str, password: str, username: str):
        super().__init__()
        self.id = str(uuid4())
        self.profile = Profile(name, email, password)
        self.account = Account(username, password)
        self.connections_sent: list["Connection"] = []
        self.posts: list["Post"] = []
        self.friends: set["User"] = set()
        self.notifications: list[Notification] = []

    def get_id(self) -> str:
        return self.id

    def get_profile(self) -> Profile:
        return self.profile

    def get_account(self) -> Account:
        return self.account

    def verify_password(self, password: str) -> bool:
        return self.account.is_valid_password(password)

    def get_name(self) -> str:
        return self.profile.get_name()

    def get_email(self) -> str:
        return self.profile.get_email()

    def get_username(self) -> str:
        return self.account.get_username()

    def get_connections(self) -> list["Connection"]:
        return self.connections_sent

    def get_posts(self) -> list["Post"]:
        return self.posts

    def get_friends(self) -> list["User"]:
        return list(self.friends)

    def get_notifications(self) -> list[Notification]:
        return self.notifications

    def add_post(self, post: "Post") -> None:
        self.posts.append(post)

    def notify(self, notification: Notification) -> None:
        print(f"Notification received: {notification.get_message()}, type: {notification.get_type().value}\n")
        self.notifications.append(notification)

    def add_to_connection_sent(self, connection: "Connection") -> None:
        self.connections_sent.append(connection)

    def remove_from_connection_sent(self, connection: "Connection") -> None:
        self.connections_sent.remove(connection)
        self.remove_friend(connection.get_to_user() if connection.get_from_user() == self else connection.get_from_user())

    def get_pending_connections(self) -> list["Connection"]:
        return [connection for connection in self.connections_sent if connection.get_status() == ConnectionStatus.PENDING]

    def add_friend(self, user: "User") -> None:
        self.friends.add(user)

    def remove_friend(self, user: "User") -> None:
        self.friends.remove(user)

    # connection observer methods
    def update_on_request_sent(self, connection: "Connection") -> None:
        if connection.get_status() != ConnectionStatus.PENDING or self not in [connection.get_from_user(), connection.get_to_user()]:
            return
        if connection.get_from_user() == self:
            message = f"{self.get_name()} have sent {connection.get_to_user().get_name()} a connection request.\n"
            notification = Notification(message, NotificationType.CONNECTION_REQUEST_SENT)
            self.notify(notification)
        elif connection.get_to_user() == self:
            message = f"{connection.get_from_user().get_name()} has sent {self.get_name()} a connection request.\n"
            notification = Notification(message, NotificationType.CONNECTION_REQUEST_SENT)
            self.notify(notification)

    def update_on_request_accepted(self, connection: "Connection") -> None:
        # check if the connection is accepted and the user is either the from user or the to user
        if connection.get_status() != ConnectionStatus.ACCEPTED or self not in [connection.get_from_user(), connection.get_to_user()]:
            return
        if connection.get_from_user() == self:
            message = f"{connection.get_to_user().get_name()} has accepted your connection request.\n"
            notification = Notification(message, NotificationType.CONNECTION_REQUEST_ACCEPTED)
            self.notify(notification)
            # add to friends
            self.add_friend(connection.get_to_user())
        elif connection.get_to_user() == self:
            message = f"{self.get_name()} and {connection.get_from_user().get_name()} are now connected.\n"
            notification = Notification(message, NotificationType.CONNECTION_REQUEST_ACCEPTED)
            self.notify(notification)
            # add to friends
            self.add_friend(connection.get_from_user())

    # post observer methods
    def on_post_created(self, post: "Post") -> None:
        print("Notified all friends on post created")
        for friend in self.get_friends():
            # Add notification to friend
            message = f"{self.get_name()} has created a new post: {post.get_content()}"
            notification = Notification(message, NotificationType.POST_CREATED)
            friend.notify(notification)

    def on_like(self, commentable: "Commentable", like: "Like") -> None:
        message = f"{like.get_user().get_name()} has liked {commentable.get_author().get_name()}'s {commentable.get_type().value}"
        notification = Notification(message, NotificationType.POST_LIKE)
        self.notify(notification)

    def on_comment(self, commentable: "Commentable", comment: "Comment") -> None:
        message = f"{comment.get_author().get_name()} has commented on {commentable.get_author().get_name()}'s {commentable.get_type().value}"
        notification = Notification(message, NotificationType.POST_COMMENT)
        self.notify(notification)
