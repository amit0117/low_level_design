from app.models.playable import Song
from app.models.artist import Artist


class SearchService:
    @staticmethod
    def search_songs_by_title(songs: list[Song], query_title: str) -> list[Song]:
        return [song for song in songs if query_title.lower() in song.title.lower()]

    @staticmethod
    def search_songs_by_artist_name(songs: list[Song], query_name: str) -> list[Song]:
        return [
            song for song in songs if query_name.lower() in song.artist.name.lower()
        ]

    @staticmethod
    def search_artists_by_name(artists: list[Artist], query_name: str) -> list[Artist]:
        return [
            artist for artist in artists if query_name.lower() in artist.name.lower()
        ]
