from typing import Any
from app.models.artist_observer import ArtistObserver

class Person(ArtistObserver):
    def __init__(self, id: str, name: str, address: Any = None, email: str = None):
        self.id = id
        self.name = name
        self.address = address
        self.email = email

    def get_name(self) -> str:
        return self.name

    def get_address(self) -> str:
        return self.address

    def set_address(self, address: Any):
        self.address = address

    def set_email(self, email: str):
        self.email = email

    def update(self, artist: 'Artist', album: 'Album'):
        if self.id != artist.id:
            print(f"Message for {self.name}")
            return super().update(artist, album)
