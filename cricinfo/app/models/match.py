from app.models.team import Team
from app.models.enums import MatchStatus, MatchType
from app.models.inning import Inning
from app.models.ball import Ball
from app.observers.match_observer import MatchSubject
from app.states.match_state import MatchState, LiveState, FinishedState
import uuid
from datetime import datetime


class Match(MatchSubject):
    # Assuming team1 is batting team and team2 is bowling team
    def __init__(self, team1: Team, team2: Team, match_type: MatchType):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.team1 = team1
        self.team2 = team2
        self.match_type = match_type
        self.innings: list[Inning] = [Inning(team1, team2)]
        self.current_state = None
        self.current_status = MatchStatus.SCHEDULED
        self.winner = None
        self.result_message = ""
        self.start_time = datetime.now()

    def get_id(self) -> str:
        return self.id

    def get_start_time(self) -> datetime:
        return self.start_time

    def get_team1(self) -> Team:
        return self.team1

    def get_team2(self) -> Team:
        return self.team2

    def get_result_message(self) -> str:
        return self.result_message

    def get_innings(self) -> list[Inning]:
        return self.innings.copy()

    def start_match(self):
        self.set_status(MatchStatus.LIVE)
        self.set_state(LiveState())

    def process_ball(self, ball: Ball):
        self.current_state.process_ball(self, ball)

    def start_next_inning(self):
        # Reverse the teams for the next innings so that the team that batted first in the previous innings bats second in the next innings
        self.current_state.start_next_inning(self)

    def end_match(self):
        if self.current_status == MatchStatus.FINISHED:
            print("Match already finished")
            return
        self.set_status(MatchStatus.FINISHED)
        self.set_state(FinishedState())
        self.update_player_statistics()

    def update_player_statistics(self):
        """Update matches played statistics for all players in both teams"""
        # Update matches played for all players in team1
        for player in self.team1.get_players():
            player.get_stats().increment_matches_played()

        # Update matches played for all players in team2
        for player in self.team2.get_players():
            player.get_stats().increment_matches_played()

    def get_current_inning(self) -> Inning:
        return self.innings[-1]

    def get_previous_inning(self) -> Inning:
        # Check if there is at least one inning
        if len(self.innings) < 2:
            return None
        return self.innings[-2]

    def create_new_inning(self, team1: Team, team2: Team):
        self.innings.append(Inning(team1, team2))

    def get_current_status(self) -> MatchStatus:
        return self.current_status

    def get_winner(self) -> Team:
        return self.winner

    def get_current_status(self) -> MatchStatus:
        return self.current_status

    def get_match_type(self) -> MatchType:
        return self.match_type

    def get_total_innings(self) -> int:
        return self.get_match_type().total_innings

    def set_state(self, state: MatchState):
        self.current_state = state

    def set_status(self, status: MatchStatus):
        self.current_status = status
        self.notify_observers(self, None)

    def set_winner(self, winner: Team):
        self.winner = winner

    def set_result_message(self, result_message: str):
        self.result_message = result_message
