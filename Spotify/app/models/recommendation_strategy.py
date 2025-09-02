from abc import ABC, abstractmethod
from app.models.playable import Song


class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, all_songs: list[Song]) -> list[Song]:
        raise NotImplementedError("Subclasses must implement recommend method")


class GenreBasedRecommendationStrategy(RecommendationStrategy):
    def recommend(self, all_songs: list[Song]) -> list[Song]:
        print("Generating genre-based recommendations...")
        # For simplicity, let's just return all songs in the same genre
        genre = all_songs[0].genre if all_songs else None
        return [song for song in all_songs if song.genre == genre][
            :3
        ]  # Return top 3 songs
