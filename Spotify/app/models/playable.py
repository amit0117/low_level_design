from abc import ABC, abstractmethod
from typing import List
from app.models.enums import SongGenre, SongTheme
from threading import Lock


class Playable(ABC):

    @abstractmethod
    def get_tracks(self) -> List["Song"]:
        raise NotImplementedError("Subclasses must implement get_tracks method")


class Song(Playable):
    def __init__(
        self,
        id: str,
        title: str,
        duration: str | int,
        artist: 'Artist',
        genre: SongGenre,
        theme: SongTheme,
    ):
        self.id = id
        self.title = title
        self.duration = duration
        self.artist = artist
        self.genre = genre
        self.theme = theme

    def get_tracks(self) -> List["Song"]:
        return [self]
    def __repr__(self):
        return f"Song(title='{self.title}', artist='{self.artist.name}')"


class Album(Playable):
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.tracks: list[Song] = []
        self.lock = Lock()
        def __repr__(self):
            return f"Album(title='{self.title}', artist='{self.artist.name}')"

    def get_title(self) -> str:
        return self.title

    def get_tracks(self) -> list[Song]:
        return self.tracks.copy()

    def add_track(self, song: Song):
        if song in self.tracks:
            print(f"Song with id {song.id} already exists in the album")
            return
        with self.lock:
            self.tracks.append(song)

    def remove_track(self, song: Song):
        with self.lock:
            self.tracks.remove(song)


class Playlist(Playable):
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title
        self.tracks: list[Song] = []
        self.lock = Lock()

    def __repr__(self):
        return f"Playlist(title='{self.title}')"

    def get_tracks(self) -> list[Song]:
        return self.tracks.copy()

    def add_track(self, song: Song):
        if song in self.tracks:
            print(f"Song with id {song.id} already exists in the playlist")
            return
        with self.lock:
            self.tracks.append(song)

    def remove_track(self, song: Song):
        with self.lock:
            self.tracks.remove(song)
