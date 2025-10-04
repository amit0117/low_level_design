from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.observers.commentable_observer import CommentableObserver
    from app.models.commentable import Commentable
    from app.models.like import Like
    from app.models.comment import Comment


class CommentableSubject:
    def __init__(self) -> None:
        self.observers: list["CommentableObserver"] = []

    def add_observer(self, observer: "CommentableObserver") -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: "CommentableObserver") -> None:
        self.observers.remove(observer)

    def notify_observers_on_like(self, commentable: "Commentable", like: "Like") -> None:
        for observer in self.observers:
            observer.on_like(commentable, like)

    def notify_observers_on_comment(self, commentable: "Commentable", comment: "Comment") -> None:
        for observer in self.observers:
            observer.on_comment(commentable, comment)
