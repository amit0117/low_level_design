from abc import ABC, abstractmethod
from app.models.enums import UserSubscription
import time
from app.models.playable import Song
from app.models.player import Player


class PlaybackStrategy(ABC):
    @abstractmethod
    def play(self, song: Song, player: Player):
        raise NotImplementedError("Subclasses must implement play method")

    @staticmethod
    def get_strategy(
        user_subscription: UserSubscription, song_played: int | None = 0
    ) -> "PlaybackStrategy":
        if user_subscription == UserSubscription.FREE:
            return FreePlaybackStrategy(song_played)
        elif user_subscription == UserSubscription.PREMIUM:
            return PremiumPlaybackStrategy()


class FreePlaybackStrategy(PlaybackStrategy):
    def __init__(self, song_played: int = 0):
        self.song_played = song_played

    def play(self, song: Song, player: Player):
        print("Playing with free strategy")
        self.song_played += 1
        if self.song_played % 3 == 0:
            # show ad for 1 sec, Simulating by time.sleep
            print("Showing ad for 1 sec. For ad-free try considering premium plan")
            time.sleep(1)
        player.set_current_song(song)


class PremiumPlaybackStrategy(PlaybackStrategy):
    def play(self, song: Song, player: Player):
        print("Playing with premium strategy")
        player.set_current_song(song)
