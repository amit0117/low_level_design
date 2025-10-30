from app.models.enums import PlayerSymbol, PlayerType
from app.models.board import Board
from app.observers.game_observer import GameObserver
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.game import Game


class Player(GameObserver):
    def __init__(self, name: str, symbol: PlayerSymbol, type: PlayerType) -> None:
        super().__init__()
        self.name = name
        self.symbol = symbol
        self.type = type

    def get_name(self) -> str:
        return self.name

    def get_symbol(self) -> str:
        return self.symbol

    def get_type(self) -> PlayerType:
        return self.type

    def update(self, game: "Game") -> None:
        print(f"Updating player {self.name} with game status: {game.get_status().value}")

    def __str__(self) -> str:
        return f"Player(name={self.name}, symbol={self.symbol})"


class ComputerPlayer(Player):
    def __init__(self, name: str, symbol: PlayerSymbol) -> None:
        super().__init__(name, symbol, PlayerType.COMPUTER)

    def __str__(self) -> str:
        return f"ComputerPlayer(name={self.name}, symbol={self.symbol})"


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: PlayerSymbol) -> None:
        super().__init__(name, symbol, PlayerType.HUMAN)

    def __str__(self) -> str:
        return f"HumanPlayer(name={self.name}, symbol={self.symbol})"
