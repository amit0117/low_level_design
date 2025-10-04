from threading import Lock
from typing import Optional
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like


class PostRepository:
    _instance: "PostRepository" = None
    _lock: Lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "posts"):
            return
        self.process_lock = Lock()
        self.posts: dict[str, Post] = {}

    @classmethod
    def get_instance(cls) -> "PostRepository":
        return cls()

    def add_post(self, post: Post) -> None:
        with self.process_lock:
            self.posts[post.get_id()] = post

    def get_post_by_id(self, post_id: str) -> Optional[Post]:
        with self.process_lock:
            return self.posts.get(post_id)

    def remove_post(self, post_id: str) -> None:
        with self.process_lock:
            if post_id not in self.posts:
                raise ValueError("Post not found")
            del self.posts[post_id]

    def get_all_posts(self) -> list[Post]:
        return list(self.posts.values())

    def get_all_posts_by_user_id(self, user_id: str) -> list[Post]:
        return [post for post in self.posts.values() if post.get_author() and post.get_author().get_id() == user_id]

    def get_all_comments_by_post_id(self, post_id: str) -> list[Comment]:
        if post_id not in self.posts:
            raise ValueError("Post not found")
        post = self.posts[post_id]
        return post.get_comments()

    def get_all_likes_by_post_id(self, post_id: str) -> list[Like]:
        if post_id not in self.posts:
            raise ValueError("Post not found")
        post = self.posts[post_id]
        return post.get_likes()
