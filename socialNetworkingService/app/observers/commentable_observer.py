from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.commentable import Commentable
    from app.models.like import Like
    from app.models.comment import Comment
    from app.models.post import Post


class CommentableObserver(ABC):
    @abstractmethod
    def on_post_created(self, post: "Post") -> None:
        raise NotImplementedError("on_post_created method is not implemented")

    @abstractmethod
    def on_like(self, commentable_entity: "Commentable", like: "Like") -> None:
        raise NotImplementedError("on_like method is not implemented")

    @abstractmethod
    def on_comment(self, commentable_entity: "Commentable", comment: "Comment") -> None:
        raise NotImplementedError("on_comment method is not implemented")
