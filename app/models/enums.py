from enum import Enum


class UserSubscription(Enum):
    FREE = "free"
    PREMIUM = "premium"


class SongGenre(Enum):
    POP = "pop"
    CLASSICAL = "classical"
    ROCK = "rock"


class SongTheme(Enum):
    HAPPY = "happy"
    SAD = "sad"
    DRAMATIC = "dramatic"
    ROMANTIC = "romantic"


# Playback status
class PlayerStatus(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
