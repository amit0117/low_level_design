from app.models.match import Match
from datetime import datetime
from app.models.enums import MatchStatus, MatchType
from app.models.team import Team
from app.models.ball import Ball
from app.observers.match_observer import MatchObserver


class MatchService:
    def __init__(self) -> None:
        self.matches: dict[str, Match] = {}

    def get_match(self, match_id: str) -> Match:
        return self.matches.get(match_id)

    def get_all_matches(self) -> list[Match]:
        return list(self.matches.values())

    def get_match_by_team(self, team_id: str) -> list[Match]:
        return [match for match in self.matches.values() if match.get_team1().get_id() == team_id or match.get_team2().get_id() == team_id]

    def get_upcoming_matches(self, time: datetime = datetime.now()) -> list[Match]:
        return [match for match in self.matches.values() if match.get_start_time() >= time]

    def get_match_by_status(self, status: MatchStatus) -> list[Match]:
        return [match for match in self.matches.values() if match.get_current_status() == status]

    def create_match(self, team1: Team, team2: Team, match_type: MatchType) -> Match:
        match = Match(team1, team2, match_type)
        self.matches[match.get_id()] = match
        return match

    def start_match(self, match_id: str):
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")
        match.start_match()

    def process_ball(self, match_id: str, ball: Ball):
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")
        match.process_ball(ball)

    def start_next_inning(self, match_id: str):
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")
        match.start_next_inning()

    def subscribe_to_match(self, match_id: str, observer: MatchObserver):
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")
        match.add_observer(observer)

    def end_match(self, match_id: str):
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")
        match.end_match()

    def search_matches_by_team_name(self, team_name: str) -> list[Match]:
        return [
            match
            for match in self.matches.values()
            if team_name.lower() in match.get_team1().get_name().lower() or team_name.lower() in match.get_team2().get_name().lower()
        ]

    def search_matches_by_match_type(self, match_type: MatchType) -> list[Match]:
        return [match for match in self.matches.values() if match.get_match_type() == match_type]

    def get_finished_matches(self) -> list[Match]:
        return self.get_match_by_status(MatchStatus.FINISHED)

    def get_live_matches(self) -> list[Match]:
        return self.get_match_by_status(MatchStatus.LIVE)

    def get_scheduled_matches(self) -> list[Match]:
        return self.get_match_by_status(MatchStatus.SCHEDULED)

    def get_match_statistics(self, match_id: str) -> dict:
        match = self.get_match(match_id)
        if match is None:
            raise ValueError(f"Match with id {match_id} not found")

        stats = {
            "match_id": match_id,
            "teams": f"{match.get_team1().get_name()} vs {match.get_team2().get_name()}",
            "match_type": match.get_match_type().name,
            "status": match.get_current_status().value,
            "total_innings": match.get_total_innings(),
            "current_inning": len(match.get_innings()) if match.get_innings() else 0,
            "result": match.get_result_message() if match.get_result_message() else "Match in progress",
        }

        if match.get_winner():
            stats["winner"] = match.get_winner().get_name()

        return stats
