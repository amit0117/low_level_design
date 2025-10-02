from app.models.player import Player
from uuid import uuid4
from threading import Lock


class Team:
    def __init__(self, name: str, players: list[Player]):
        self.id = str(uuid4())
        self.name = name
        self.players = players
        self.matches_won = 0
        self.matches_lost = 0
        self.lock = Lock()

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_players(self) -> list[Player]:
        return self.players.copy()

    def get_matches_won(self) -> int:
        return self.matches_won

    def get_matches_lost(self) -> int:
        return self.matches_lost

    def add_player(self, player: Player) -> None:
        with self.lock:
            self.players.append(player)

    def remove_player(self, player_id: str) -> None:
        with self.lock:
            for player in self.players:
                if player.get_id() == player_id:
                    self.players.remove(player)
                    return
        raise ValueError(f"Player {player_id} not found in team {self.get_name()}")

    def find_player(self, player_id: str) -> Player:
        for player in self.players:
            if player.get_id() == player_id:
                return player
        raise ValueError(f"Player {player_id} not found in team {self.get_name()}")

    def increment_matches_won(self) -> None:
        with self.lock:
            self.matches_won += 1

    def increment_matches_lost(self) -> None:
        with self.lock:
            self.matches_lost += 1

    def __str__(self) -> str:
        return f"Team {self.get_name()} (ID: {self.get_id()}), current players: [{', '.join([player.get_name() for player in self.get_players()])}]"
