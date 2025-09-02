from app.models.recommendation_strategy import RecommendationStrategy
from app.models.playable import Song


class RecommendationService:
    def __init__(self, strategy: RecommendationStrategy):
        self.strategy = strategy

    def recommend(self, all_songs: list[Song]) -> list[Song]:
        return self.strategy.recommend(all_songs)
