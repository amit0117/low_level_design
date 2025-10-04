from app.models.commentable import Commentable
from typing import TYPE_CHECKING
from app.models.enums import CommentableType

if TYPE_CHECKING:
    from app.models.user import User


class Post(Commentable):
    def __init__(self, author: "User", content: str) -> None:
        super().__init__(author, content)

    def get_type(self) -> CommentableType:
        return CommentableType.POST
