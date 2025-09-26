from app.services.game_service import GameService
from app.services.player_service import PlayerService
from app.services.board_service import BoardService
from app.models.game import Game
import threading


class SnakeAndLadderGame:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return
        self.initialized = True
        self.game_service = GameService()
        self.player_service = PlayerService()
        self.board_service = BoardService()
        self._processing_lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        return cls()

    def create_new_game(self, player_names: list[str],board_size: int = 100) -> Game:
        with self._processing_lock:
            board = self.board_service.create_board(board_size)
            players = self.player_service.create_players(player_names)
            return self.game_service.create_game(board, players)

    def play_game(self, game_id: str):
        with self._processing_lock:
            game = self.game_service.get_game_by_id(game_id)
            game.play()
