from app.models.enums import UserSubscription
from app.models.artist import Artist
from app.models.person import Person
from app.models.playback_strategy import PlaybackStrategy


class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code


class User(Person):
    def __init__(self, id, name=None, address=None, email=None):
        super().__init__(id, name, address, email)
        self.subscription_tier: UserSubscription = UserSubscription.FREE
        self.followed_artists: set[Artist] = set()
        self.playback_strategy: PlaybackStrategy | None = None


    def get_name(self) -> str:
        return self.name

    def follow_artist(self, artist: Artist):
        self.followed_artists.add(artist)
        print(f"{self.name} has added {artist.name} to their followed artists list.")
        artist.subject.add_observer(self)

    def get_playback_strategy(self) -> PlaybackStrategy | None:
        if self.playback_strategy is None:
            self.playback_strategy = PlaybackStrategy.get_strategy(self.subscription_tier)
        return self.playback_strategy



class UserBuilder:
    def __init__(self, user: User):
        self.user = user

    def add_name(self, name: str) -> "UserBuilder":
        self.user.name = name
        return self

    def add_address(self, address: Address) -> "UserBuilder":
        self.user.address = address
        return self

    def add_email(self, email: str) -> "UserBuilder":
        self.user.email = email
        return self

    def add_subscription(self, subscription: UserSubscription) -> "UserBuilder":
        self.user.subscription_tier = subscription
        return self

    def build(self) -> User:
        return self.user
