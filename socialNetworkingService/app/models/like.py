from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.commentable import Commentable


class Like:
    def __init__(self, user: "User", commentable: "Commentable") -> None:
        self.user = user
        self.commentable = commentable
        self.timestamp = datetime.now()

    def get_user(self) -> "User":
        return self.user

    def get_commentable(self) -> "Commentable":
        return self.commentable
