from app.models.playable import Album
from typing import List


class ArtistObserver:
    # Create a default implementation for the update method
    # And any concrete observer may override this method if necessary
    def update(self, artist: 'Artist', album: Album):
        print(f"Artist: {artist.get_name()} has released album: {album.get_title()}")


class Subject:

    def __init__(self):
        self.observers: List[ArtistObserver] = []

    def add_observer(self, observer: ArtistObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: ArtistObserver):
        self.observers.remove(observer)

    def notify_observers(self, artist: 'Artist', album: Album):
        for observer in self.observers:
            observer.update(artist, album)
