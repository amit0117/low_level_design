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


class EngagementBasedStrategy(NewsFeedGenerationStrategy):
    """
    Recommends posts based on user engagement (likes, comments)
    Priority: Posts with higher engagement from friends
    """

    def generate_feed(self, user: User) -> List[Post]:
        friends = user.get_friends()
        feed: list[Post] = []

        for friend in friends:
            feed.extend(friend.get_posts()[:20])  # Get more posts to score

        # Score posts based on engagement (likes + comments)
        scored_posts = []
        for post in feed:
            engagement_score = len(post.get_likes()) + len(post.get_comments())
            scored_posts.append((post, engagement_score))

        # Sort by engagement score (descending)
        scored_posts.sort(key=lambda x: x[1], reverse=True)

        # Return top 10 most engaging posts
        return [post for post, score in scored_posts][:10]


class InterestBasedStrategy(NewsFeedGenerationStrategy):
    """
    Recommends posts based on user's interests and past engagement
    Priority: Posts containing keywords user has engaged with before
    """

    def generate_feed(self, user: User) -> List[Post]:
        friends = user.get_friends()
        feed: list[Post] = []

        # Collect user's interests based on past likes/comments
        user_interests = self._extract_user_interests(user)

        for friend in friends:
            feed.extend(friend.get_posts()[:15])

        # Score posts based on interest matching
        scored_posts = []
        for post in feed:
            content = post.get_content().lower()
            interest_score = sum(1 for interest in user_interests if interest.lower() in content)
            scored_posts.append((post, interest_score))

        # Sort by interest score (descending), then by recency
        scored_posts.sort(key=lambda x: (x[1], x[0].get_timestamp()), reverse=True)

        return [post for post, score in scored_posts][:10]

    def _extract_user_interests(self, user: User) -> List[str]:
        """Extract user's interests from liked posts and comments"""
        interests = set()

        # Check liked posts for keywords
        for post in user.get_liked_posts():
            words = post.get_content().split()
            # Extract meaningful keywords (words longer than 3 chars)
            interests.update(word for word in words if len(word) > 3)

        # Check user's own posts for interests
        for post in user.get_posts():
            words = post.get_content().split()
            interests.update(word for word in words if len(word) > 3)

        return list(interests)


class PopularityBasedStrategy(NewsFeedGenerationStrategy):
    """
    Recommends posts based on overall popularity across the platform
    Priority: Posts with highest likes/comments regardless of friendship
    """

    def generate_feed(self, user: User) -> List[Post]:
        friends = user.get_friends()
        feed: list[Post] = []

        for friend in friends:
            feed.extend(friend.get_posts()[:15])

        # Also include some posts from friends of friends for broader reach
        friends_of_friends_posts = []
        for friend in friends:
            for friend_of_friend in friend.get_friends():
                if friend_of_friend != user and friend_of_friend not in friends:
                    friends_of_friends_posts.extend(friend_of_friend.get_posts()[:5])

        feed.extend(friends_of_friends_posts[:10])  # Limit to avoid too many posts

        # Score posts based on total engagement
        scored_posts = []
        for post in feed:
            popularity_score = len(post.get_likes()) * 2 + len(post.get_comments()) * 3  # Weight comments higher
            scored_posts.append((post, popularity_score))

        # Sort by popularity score (descending)
        scored_posts.sort(key=lambda x: x[1], reverse=True)

        return [post for post, score in scored_posts][:10]


class MixedStrategy(NewsFeedGenerationStrategy):
    """
    Combines multiple strategies for balanced recommendations
    Uses 40% chronological, 30% engagement, 30% interest-based
    """

    def __init__(self):
        self.chronological = ChronologicalStrategy()
        self.engagement = EngagementBasedStrategy()
        self.interest = InterestBasedStrategy()

    def generate_feed(self, user: User) -> List[Post]:
        # Get feeds from different strategies
        chrono_feed = self.chronological.generate_feed(user)
        engage_feed = self.engagement.generate_feed(user)
        interest_feed = self.interest.generate_feed(user)

        # Combine with weights
        combined_feed = []
        combined_feed.extend(chrono_feed[:4])  # 40% chronological
        combined_feed.extend(engage_feed[:3])  # 30% engagement
        combined_feed.extend(interest_feed[:3])  # 30% interest

        # Remove duplicates while preserving order
        seen = set()
        unique_feed = []
        for post in combined_feed:
            if post.get_id() not in seen:
                seen.add(post.get_id())
                unique_feed.append(post)

        return unique_feed[:10]
