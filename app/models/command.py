from abc import ABC, abstractmethod
from app.models.player import Player


class Command(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute method")


# Different Playback commands
# play,pause,togglePlayPause, nextTrack, previousTrack, changePlaybackSpeed, changePlayBackPosition (seekForward, seekBackward:- Allow user to jump to the specific position in the track)


class PlayCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_play()


class PauseCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_pause()


class StopCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_stop()


class NextTrackCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_next()


class PreviousTrackCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_previous()


class TogglePlayPauseCommand(Command):
    def __init__(self, player: Player):
        self.player = player

    def execute(self):
        self.player.click_play_pause()
