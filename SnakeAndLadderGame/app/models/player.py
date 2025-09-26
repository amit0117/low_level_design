from app.models.cell import Cell
from uuid import uuid4
from app.observers.game_observer import GameObserver
from app.models.enums import GameStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import Game


class Player(GameObserver):
    def __init__(self, name: str, position: Cell) -> None:
        super().__init__()
        self.id = uuid4()
        self.name = name
        self.current_position: Cell = position
        self.games: list["Game"] = []

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_current_position(self) -> Cell:
        return self.current_position

    def set_current_position(self, position: Cell) -> None:
        self.current_position = position

    def add_game(self, game: "Game") -> None:
        self.games.append(game)

    def remove_game(self, game: "Game") -> None:
        if game not in self.games:
            raise ValueError("Game not found in the player's games")
        self.games.remove(game)

    def get_all_games(self) -> list["Game"]:
        return self.games

    def update(self, game: "Game") -> None:
        print("Message from game with id", game.get_id(), "to player", self.get_name())
        if game.get_status() == GameStatus.FINISHED:
            if game.get_winner() is None:
                print("Game with id", game.get_id(), "is finished, but no winner is declared")
            else:
                if self == game.get_winner():
                    print("You are the winner of the game with id", game.get_id())
                else:
                    print("Player", game.get_winner().get_name(), "is the winner of the game with id", game.get_id())
