from threading import Lock
from app.services.match_service import MatchService
from app.services.player_service import PlayerService
from app.services.commentary_service import CommentaryService
from app.observers.match_observer import ScorecardDisplay, UserNotifier, CommentaryManager
from app.models.enums import MatchType, PlayerRole
from app.models.team import Team
from app.models.match import Match
from app.models.ball import Ball
from app.observers.match_observer import MatchObserver
from app.models.player import Player


class CricInfoService:
    _instance = None
    _lock = Lock()

    def __new__(cls) -> "CricInfoService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_has_initialized"):
            return
        self._has_initialized = True
        self.match_service = MatchService()
        self.player_service = PlayerService()
        self.commentary_service = CommentaryService()

    @classmethod
    def get_instance(cls) -> "CricInfoService":
        return cls()

    def create_match(self, team1: Team, team2: Team, match_type: MatchType) -> Match:
        match = self.match_service.create_match(team1, team2, match_type)
        return match

    def start_match(self, match_id: str) -> None:
        self.match_service.start_match(match_id)

    def process_ball(self, match_id: str, ball: Ball) -> None:
        self.match_service.process_ball(match_id, ball)

    def end_match(self, match_id: str) -> None:
        self.match_service.end_match(match_id)

    def subscribe_to_match(self, match_id: str, observer: MatchObserver) -> None:
        self.match_service.subscribe_to_match(match_id, observer)

    def start_next_inning(self, match_id: str) -> None:
        self.match_service.start_next_inning(match_id)

    def add_player(self, name: str, country: str, role: PlayerRole) -> Player:
        return self.player_service.create_player(name, country, role)

    # Search functionality - orchestrating other services
    def search_matches_by_team(self, team_name: str) -> list[Match]:
        """Search for matches involving a specific team by name"""
        return self.match_service.search_matches_by_team_name(team_name)

    def search_matches_by_type(self, match_type: MatchType) -> list[Match]:
        """Search for matches by match type"""
        return self.match_service.search_matches_by_match_type(match_type)

    def search_players_by_name(self, name_pattern: str) -> list[Player]:
        """Search for players by name pattern"""
        return self.player_service.search_players_by_name(name_pattern)

    def search_players_by_country(self, country: str) -> list[Player]:
        """Search for players by country"""
        return self.player_service.search_players_by_country(country)

    def search_players_by_role(self, role: PlayerRole) -> list[Player]:
        """Search for players by role"""
        return self.player_service.search_players_by_role(role)

    # Match history and status methods
    def get_match_history(self) -> list[Match]:
        """Get all matches in the system"""
        return self.match_service.get_all_matches()

    def get_finished_matches(self) -> list[Match]:
        """Get all finished matches"""
        return self.match_service.get_finished_matches()

    def get_upcoming_matches(self) -> list[Match]:
        """Get all upcoming/scheduled matches"""
        return self.match_service.get_scheduled_matches()

    def get_live_matches(self) -> list[Match]:
        """Get all live matches"""
        return self.match_service.get_live_matches()

    # Detailed information methods
    def get_match_details(self, match_id: str) -> dict:
        """Get detailed information about a match"""
        return self.match_service.get_match_statistics(match_id)

    def get_player_details(self, player_id: str) -> dict:
        """Get detailed information about a player"""
        return self.player_service.get_player_statistics(player_id)
