from app.models.player import Player
from app.models.enums import PlayerRole


class PlayerService:
    def __init__(self) -> None:
        self.players: dict[str, Player] = {}

    def get_player(self, player_id: str) -> Player:
        return self.players.get(player_id)

    def get_all_players(self) -> list[Player]:
        return list(self.players.values())

    def create_player(self, name: str, country: str, role: PlayerRole) -> Player:
        player = Player(name, country, role)
        self.players[player.get_id()] = player
        return player

    def search_players_by_name(self, name_pattern: str) -> list[Player]:
        """Search for players by name pattern"""
        return [player for player in self.players.values() if name_pattern.lower() in player.get_name().lower()]

    def search_players_by_country(self, country: str) -> list[Player]:
        """Search for players by country"""
        return [player for player in self.players.values() if player.get_country().lower() == country.lower()]

    def search_players_by_role(self, role: PlayerRole) -> list[Player]:
        """Search for players by role"""
        return [player for player in self.players.values() if player.get_role() == role]

    def get_player_statistics(self, player_id: str) -> dict:
        """Get detailed statistics for a player"""
        player = self.get_player(player_id)
        if player is None:
            raise ValueError(f"Player with id {player_id} not found")

        stats = player.get_stats()
        return {
            "player_id": player_id,
            "name": player.get_name(),
            "country": player.get_country(),
            "role": player.get_role().value,
            "runs_scored": stats.get_runs(),
            "balls_faced": stats.get_balls_faced(),
            "wickets_taken": stats.get_wickets_taken(),
            "balls_bowled": stats.get_balls_bowled(),
            "matches_played": stats.get_matches_played(),
        }
