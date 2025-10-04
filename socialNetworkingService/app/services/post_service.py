from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like


class PostService:
    def __init__(self):
        self.post_repository = PostRepository.get_instance()
        self.user_repository = UserRepository.get_instance()

    def create_post(self, user_id: str, content: str) -> Post:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        post = Post(user, content)
        self.post_repository.add_post(post)
        user.add_post(post)  # Add post to user's post list
        return post

    def like_post(self, user_id: str, post_id: str) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        like = Like(user, post)
        post.add_like(like)

    def add_comment(self, user_id: str, post_id: str, content: str) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        post = self.post_repository.get_post_by_id(post_id)
        if not post:
            raise ValueError(f"Post with ID {post_id} not found")
        comment = Comment(user, content)
        post.add_comment(comment)

    def get_post_by_id(self, post_id: str) -> Post:
        return self.post_repository.get_post_by_id(post_id)

    def get_all_posts(self) -> list[Post]:
        return self.post_repository.get_all_posts()

    def get_all_posts_by_user_id(self, user_id: str) -> list[Post]:
        return self.post_repository.get_all_posts_by_user_id(user_id)

    def get_all_comments_by_post_id(self, post_id: str) -> list[Comment]:
        return self.post_repository.get_all_comments_by_post_id(post_id)

    def get_all_comments(self, post_id: str) -> list[Comment]:
        return self.post_repository.get_all_comments_by_post_id(post_id)

    def get_all_likes(self, post_id: str) -> list[Like]:
        return self.post_repository.get_all_likes_by_post_id(post_id)
