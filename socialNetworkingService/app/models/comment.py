from app.models.commentable import Commentable
from typing import TYPE_CHECKING
from app.models.enums import CommentableType

if TYPE_CHECKING:
    from app.models.user import User


class Comment(Commentable):
    def __init__(self, author: "User", content: str) -> None:
        Commentable.__init__(self, author, content)

    def get_replies(self) -> list["Comment"]:
        return self.get_comments()

    def get_type(self) -> str:
        return CommentableType.COMMENT
