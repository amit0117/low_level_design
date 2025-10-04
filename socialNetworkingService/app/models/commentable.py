from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from abc import ABC, abstractmethod
from app.models.enums import CommentableType
from app.observers.commentable_subject import CommentableSubject

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.comment import Comment
    from app.models.like import Like


class Commentable(ABC, CommentableSubject):
    def __init__(self, author: "User", content: str) -> None:
        CommentableSubject.__init__(self)
        self.id = str(uuid.uuid4())
        self.author = author
        self.content = content
        self.timestamp = datetime.now()
        self.likes: list["Like"] = []
        self.comments: list["Comment"] = []

    @abstractmethod
    def get_type(self) -> CommentableType:
        raise NotImplementedError("get_type method is not implemented")

    def get_id(self) -> str:
        return self.id

    def get_content(self) -> str:
        return self.content

    def get_author(self) -> "User":
        return self.author

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def get_likes(self) -> list["Like"]:
        return self.likes

    def get_comments(self) -> list["Comment"]:
        return self.comments

    def add_like(self, like: "Like") -> None:
        # First notify the already existing observers
        self.notify_observers_on_like(self, like)
        # add the like author to the like subject
        self.add_observer(like.get_user())
        # add the like to the likes list
        self.likes.append(like)

    def add_comment(self, comment: "Comment") -> None:
        # First notify the already existing observers
        self.notify_observers_on_comment(self, comment)
        # add the comment author to the comment subject
        self.add_observer(comment.get_author())
        # add the comment to the comments list
        self.comments.append(comment)
