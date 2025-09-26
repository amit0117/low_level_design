from abc import ABC, abstractmethod
from app.models.enums import GameStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import Game


class GameState(ABC):
    @abstractmethod
    def play(self, game: "Game"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def pause(self, game: "Game"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def resume(self, game: "Game"):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def stop(self, game: "Game"):
        raise NotImplementedError("Subclasses must implement this method")


class NotStartedState(GameState):
    def play(self, game: "Game"):
        if len(game.get_players()) < 2:
            print("Cannot start game. At least 2 players are required.")
            return
        game.setStatus(GameStatus.RUNNING)
        game.setState(RunningState())

        # Run the game until it is finished
        while game.get_status() == GameStatus.RUNNING:
            game.make_move()

    def pause(self, game: "Game"):
        print("Game has not started yet, Can't pause")

    def resume(self, game: "Game"):
        print("Game has not started yet, Can't resume")

    def stop(self, game: "Game"):
        print("Game is in not started state, Can't stop")


class RunningState(GameState):
    def play(self, game: "Game"):
        print("Game is already running, Can't Re-Play")

    def pause(self, game: "Game"):
        print("Game with id", game.get_id(), "status changed from running to paused")
        game.setStatus(GameStatus.PAUSED)
        game.setState(PausedState())

    def resume(self, game: "Game"):
        print("Game is already running, Can't resume")

    def stop(self, game: "Game"):
        print("Game with id", game.get_id(), "status changed from running to finished")
        game.setStatus(GameStatus.FINISHED)
        game.setState(FinishedState())


class PausedState(GameState):
    def play(self, game: "Game"):
        print("Game is paused, Can't play")

    def pause(self, game: "Game"):
        print("Game is already paused, Can't pause")

    def resume(self, game: "Game"):
        print("Game with id", game.get_id(), "status changed from paused to running")
        game.setStatus(GameStatus.RUNNING)
        game.setState(RunningState())

    def stop(self, game: "Game"):
        print("Game with id", game.get_id(), "status changed from paused to finished")
        game.setStatus(GameStatus.FINISHED)
        game.setState(FinishedState())


class FinishedState(GameState):
    def play(self, game: "Game"):
        print("Game is finished, Can't play")

    def pause(self, game: "Game"):
        print("Game is finished, Can't pause")

    def resume(self, game: "Game"):
        print("Game is finished, Can't resume")

    def stop(self, game: "Game"):
        print("Game is finished, Can't stop")
