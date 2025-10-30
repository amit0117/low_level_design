from abc import ABC, abstractmethod
from app.models.enums import GameStatus
from app.models.player import Player
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import Game


class GameState(ABC):
    @abstractmethod
    def start(self, game: "Game") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def make_move(self, game: "Game", player: Player, row: int, col: int) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def end(self, game: "Game") -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_winner(self, game: "Game") -> Optional[Player]:
        raise NotImplementedError("Subclasses must implement this method")


class NotStartedState(GameState):
    def start(self, game: "Game") -> None:
        print("Starting the game with players: ", [player.get_name() for player in game.get_players()])
        game.set_status(GameStatus.IN_PROGRESS)
        game.set_state(InProgressState())

    def make_move(self, game: "Game", player: Player, row: int, col: int) -> None:
        raise NotImplementedError("Game is not started yet, can't make a move")

    def end(self, game: "Game") -> None:
        raise NotImplementedError("Game is not started yet, can't end")

    def get_winner(self, game: "Game") -> Optional[Player]:
        raise NotImplementedError("Game is not started yet, no winner yet")


class InProgressState(GameState):
    def start(self, game: "Game") -> None:
        raise NotImplementedError("Game is already in progress, can't start again")

    def make_move(self, game: "Game", player: Player, row: int, col: int) -> None:
        if game.get_board().make_move(row, col, player.get_symbol()):
            if game.check_winner(player, row, col):
                game.set_winner(player)
                game.set_status(GameStatus.COMPLETED)
                game.set_state(CompletedState())
            elif game.check_for_draw():
                game.set_status(GameStatus.COMPLETED)
                game.set_state(CompletedState())
        else:
            raise ValueError("Invalid move!")

    def end(self, game: "Game") -> None:
        print("Stopping the game with players: ", [player.get_name() for player in game.get_players()])
        game.set_status(GameStatus.COMPLETED)
        game.set_state(CompletedState())

    def get_winner(self, game: "Game") -> Optional[Player]:
        raise NotImplementedError("Game is already started, can't get winner")


class CompletedState(GameState):
    def start(self, game: "Game") -> None:
        raise NotImplementedError("Game is already completed, can't start again")

    def make_move(self, game: "Game", player: Player, row: int, col: int) -> None:
        raise NotImplementedError("Game is already completed, can't make a move")

    def end(self, game: "Game") -> None:
        raise NotImplementedError("Game is already completed, can't end")

    def get_winner(self, game: "Game") -> Optional[Player]:
        return game.winner
