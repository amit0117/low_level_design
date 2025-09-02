from abc import ABC, abstractmethod
from app.models.enums import PlayerStatus


class PlayerState(ABC):
    @abstractmethod
    def play(self, player: "Player"):
        raise NotImplementedError("Subclasses must implement play function")

    @abstractmethod
    def pause(self, player: "Player"):
        raise NotImplementedError("Subclasses must implement pause function")

    @abstractmethod
    def stop(self, player: "Player"):
        raise NotImplementedError("Subclasses must implement stop function")

    @abstractmethod
    def toggle_play_pause(self, player: "Player"):
        raise NotImplementedError(
            "Subclasses must implement toggle_play_pause function"
        )


class PauseState(PlayerState):
    def play(self, player: "Player"):
        print("Resuming playback")
        player.set_state(PlayingState())
        player.set_status(PlayerStatus.PLAYING)

    def pause(self, player: "Player"):
        print("Playback is already paused")

    def stop(self, player: "Player"):
        print("Stopping the playback")
        player.set_state(StoppedState())
        player.set_status(PlayerStatus.STOPPED)

    def toggle_play_pause(self, player: "Player"):
        print("Toggling playback from paused to playing")
        player.set_state(PlayingState())
        player.set_status(PlayerStatus.PLAYING)


class PlayingState(PlayerState):
    def play(self, player: "Player"):
        # Check if the player has song and is currently no song is selected
        if player.has_queue() and player.current_index == -1:
            player.set_current_song(player.queue[0])
        # Play song if available
        if player.has_queue():
            player.play_current_song_in_queue()
        else:
            print("No tracks in queue. Load some tracks first.")

    def pause(self, player: "Player"):
        print("Pausing playback")
        player.set_state(PauseState())
        player.set_status(PlayerStatus.PAUSED)

    def stop(self, player: "Player"):
        print("Stopping the playback")
        player.set_state(StoppedState())
        player.set_status(PlayerStatus.STOPPED)

    def toggle_play_pause(self, player: "Player"):
        print("Toggling playback from playing to paused")
        player.set_state(PauseState())
        player.set_status(PlayerStatus.PAUSED)


class StoppedState(PlayerState):
    def play(self, player: "Player"):
        print("Starting playback from stopped state:")
        player.set_state(PlayingState())
        player.set_status(PlayerStatus.PLAYING)
        player.click_play()

    def pause(self, player: "Player"):
        print("Can't pause, Player is stopped")

    def stop(self, player: "Player"):
        print("Playback is already stopped")

    def toggle_play_pause(self, player: "Player"):
        print("Player is stopped, cannot toggle play/pause")
