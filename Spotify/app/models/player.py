from app.models.player_states import PlayerState, StoppedState
from app.models.enums import PlayerStatus
from app.models.playable import Song
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.playable import Playable


class Player:
    def __init__(self):
        self.state = StoppedState()
        self.status = PlayerStatus.STOPPED
        self.queue: list[Song] = []
        self.current_song: Optional[Song] = None
        self.current_index: int = -1
        self.current_user: Optional["User"] = None

    def load(self, user: "User", playable: "Playable"):
        self.current_user = user
        self.queue = playable.get_tracks()
        self.current_song = None
        self.current_index = -1
        self.status = PlayerStatus.STOPPED
        self.state = StoppedState()

    def set_state(self, state: PlayerState):
        self.state = state

    def set_status(self, status: PlayerStatus):
        self.status = status

    def set_current_song(self, song: Song):
        for i, s in enumerate(self.queue):
            if s.id == song.id:
                self.current_index = i
                break

        if self.current_index == -1:
            print(f"Song :{song.title} doesn't exist in current queue.")
            return

        self.current_song = song

    def click_play(self):
        self.state.play(self)

    def click_pause(self):
        self.state.pause(self)

    def click_stop(self):
        self.state.stop(self)

    def click_play_pause(self):
        self.state.toggle_play_pause(self)

    def click_next(self):
        if self.current_index + 1 < len(self.queue):
            self.current_index += 1
            self.current_song = self.queue[self.current_index]
        else:
            # We may want to loop back to the start of the queue
            print("Reached end of queue")

    def click_previous(self):
        if self.current_index - 1 >= 0:
            self.current_index -= 1
            self.current_song = self.queue[self.current_index]
        else:
            # We may want to loop back to the end of the queue
            print("Reached start of queue")

    def has_queue(self):
        return len(self.queue) > 0

    def play_current_song_in_queue(self):
        print(f"Playing song at index: {self.current_index+1}")
        # Play the current song in the queue
        if self.current_song:
            self.current_user.get_playback_strategy().play(self.current_song, self)
            print(f"Playing song: {self.current_song.title} by artist: {self.current_song.artist.name}")
        else:
            print("No song is currently loaded.")
