from app.models.person import Person
from app.models.playable import Album
from typing import List
from app.models.artist_observer import Subject


class Artist(Person):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.albums: List[Album] = []
        self.subject = Subject()

    def release_album(self, album: Album):
        self.albums.append(album)
        # notify all follower that this artist has released an album
        self.subject.notify_observers(self, album)

    def add_follower(self, follower: Person):
        self.subject.add_observer(follower)
