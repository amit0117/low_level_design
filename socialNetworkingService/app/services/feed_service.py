from app.strategies.feed_generation_strategy import NewsFeedGenerationStrategy, ChronologicalStrategy
from app.models.user import User
from app.models.post import Post


class FeedService:
    def __init__(self):
        # default strategy
        self.strategy = ChronologicalStrategy()

    def set_strategy(self, strategy: NewsFeedGenerationStrategy):
        self.strategy = strategy

    def get_feed(self, user: User) -> list[Post]:
        return self.strategy.generate_feed(user)
