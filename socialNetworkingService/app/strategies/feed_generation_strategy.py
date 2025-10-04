from abc import ABC, abstractmethod
from app.models.user import User
from typing import List
from app.models.post import Post


class NewsFeedGenerationStrategy(ABC):
    @abstractmethod
    def generate_feed(self, user: User) -> List[Post]:
        raise NotImplementedError("generate_feed method is not implemented")


class ChronologicalStrategy(NewsFeedGenerationStrategy):
    def generate_feed(self, user: User) -> List[Post]:
        friends = user.get_friends()
        feed: list[Post] = []

        for friend in friends:
            feed.extend(friend.get_posts()[:10])

        # Sort posts by timestamp in reverse (most recent first)
        feed.sort(key=lambda p: p.get_timestamp(), reverse=True)

        # Return top 10 posts
        return feed[:10]
