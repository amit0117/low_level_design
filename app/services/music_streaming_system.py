from app.models.user import User
from app.models.artist import Artist
from app.models.playable import Song
from app.models.player import Player
from app.models.recommendation_strategy import (
    GenreBasedRecommendationStrategy,
)
from app.services.recommendation_service import RecommendationService
from app.services.search_service import SearchService
from app.services.user_service import UserService
from threading import Lock


class MusicStreamingSystem:
    _instance = None
    _has_initialized = None
    _lock = Lock()

    def __new__(cls):
        # Double Lock Check Singleton Pattern
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._has_initialized = False
        return cls._instance

    def __init__(self):
        if not self._has_initialized:
            self.users: dict[str, User] = {}
            self.artists: dict[str, Artist] = {}
            self.songs: dict[str, Song] = {}
            self.player: Player = Player()
            self.recommendation_service = RecommendationService(
                GenreBasedRecommendationStrategy()
            )
            self.search_service = SearchService()
            self.user_service = UserService()
            self._has_initialized = True

    # Use class method instead of static method for better structure as if we use classMethod we may use this function to get the instance of child class
    # But if we use static method then we have hardcoded that with the current class only and that function is not extensible
    @classmethod
    def get_instance(cls):
        return cls()

    def add_song(self, song: Song):
        if song.id in self.songs:
            print(f"Song with id {song.id} already exists")
            return  # Song is already added
        with self.__class__._lock:
            self.songs[song.id] = song

    def remove_song(self, song: Song):
        if song.id not in self.songs:
            print(f"Song with id {song.id} does not exist")
            return
        with self.__class__._lock:
            del self.songs[song.id]

    def get_player(self) -> Player:
        return self.player

    def get_all_songs(self) -> list[Song]:
        return list(self.songs.values())

    def get_all_users(self) -> list[User]:
        return list(self.users.values())

    def get_all_artists(self) -> list[Artist]:
        return list(self.artists.values())

    def get_song_recommendations(self) -> list[Song]:
        all_songs = self.get_all_songs()
        return self.recommendation_service.recommend(all_songs)

    def search_songs_by_title(self, query: str) -> list[Song]:
        all_songs = self.get_all_songs()
        return self.search_service.search_songs_by_title(all_songs, query)

    def search_songs_by_artist_name(self, query: str) -> list[Song]:
        all_songs = self.get_all_songs()
        return self.search_service.search_songs_by_artist_name(all_songs, query)

    def search_artists_by_name(self, query: str) -> list[Artist]:
        all_artists = self.get_all_artists()
        return self.search_service.search_artists_by_name(all_artists, query)

    def add_new_user(self, user: User):
        self.user_service.register_user(user)

    def remove_user(self, user: User):
        self.user_service.remove_user(user)

    def add_new_artist(self, artist: Artist):
        self.user_service.register_artist(artist)

    def remove_artist(self, artist: Artist):
        self.user_service.remove_artist(artist)

    def get_user_by_id(self, id: str) -> User | None:
        return self.users.get(id)

    def get_artist_by_id(self, id: str) -> Artist | None:
        return self.artists.get(id)
