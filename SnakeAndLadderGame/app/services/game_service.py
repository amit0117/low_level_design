from app.models.game import Game
from typing import Optional
from app.models.board import Board
from app.models.player import Player


class GameService:
    def __init__(self) -> None:
        self.games: list[Game] = []

    def remove_game(self, game: Game) -> None:
        if game not in self.games:
            raise ValueError("Game not found")
        self.games.remove(game)

    def get_game_by_id(self, game_id: str) -> Optional[Game]:
        for game in self.games:
            if game.get_id() == game_id:
                return game
        return None

    def get_all_games(self) -> list[Game]:
        return self.games

    def create_game(self, board: Board, players: list[Player]) -> Game:
        game = Game(board, players)
        self.games.append(game)
        return game
