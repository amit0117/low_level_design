from app.models.enums import PlayerRole
from app.models.player_stats import PlayerStats
from uuid import uuid4


class Player:
    def __init__(self, name: str, country: str, role: PlayerRole):
        self.id = str(uuid4())
        self.name = name
        self.country = country
        self.role = role
        self.stats = PlayerStats()

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_country(self) -> str:
        return self.country

    def get_role(self) -> PlayerRole:
        return self.role

    def get_stats(self) -> PlayerStats:
        return self.stats

    def update_stats(self, stats: PlayerStats) -> None:
        self.stats = stats
