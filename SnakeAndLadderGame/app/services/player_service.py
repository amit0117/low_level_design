from app.models.player import Player
from app.models.cell import Cell
from typing import Optional


class PlayerService:
    def __init__(self) -> None:
        self.players: list[Player] = []

    def create_players(self, player_names: list[str]) -> list[Player]:
        for name in player_names:
            self.players.append(Player(name, Cell(0)))
        return self.players[len(self.players) - len(player_names) :]

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def remove_player(self, player: Player) -> None:
        if player not in self.players:
            raise ValueError("Player not found")
        self.players.remove(player)

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        for player in self.players:
            if player.get_id() == player_id:
                return player
        return None

    def get_player_by_name(self, player_name: str) -> Optional[Player]:
        for player in self.players:
            if player.get_name() == player_name:
                return player
        return None

    def get_all_players(self) -> list[Player]:
        return self.players
