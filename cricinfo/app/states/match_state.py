from abc import ABC, abstractmethod
from app.models.ball import Ball
from app.models.team import Team
from app.models.enums import MatchStatus
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.match import Match


class MatchState(ABC):
    @abstractmethod
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        print("ERROR: Cannot process a ball from the current state.")

    @abstractmethod
    def start_next_inning(self, match: "Match"):
        print("ERROR: Cannot start the next innings from the current state.")


class ScheduledState(MatchState):
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        print("ERROR: Cannot process a ball from the scheduled state.")

    def start_next_inning(self, match: "Match"):
        print("ERROR: Cannot start the next innings from the scheduled state.")


class LiveState(MatchState):
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        if ball is None:
            print("ERROR: Ball is None.")
            return
        if len(match.get_innings()) == 0:
            print("ERROR: No innings to process the ball.")
            return
        current_innings = match.get_current_inning()
        current_innings.add_ball(ball)
        match.notify_observers(match, ball)
        self.check_for_match_end(match)

    def _is_final_innings(self, match: "Match"):
        innings_count = len(match.get_innings())
        return innings_count == match.get_total_innings()

    def _is_all_out(self, match: "Match"):
        return match.get_current_inning().get_wickets() >= len(match.get_current_inning().get_batting_team().get_players()) - 1

    def _are_overs_finished(self, match: "Match"):
        return match.get_current_inning().get_overs_till_now() >= match.get_match_type().total_overs_per_innings

    def check_for_match_end(self, match: "Match") -> None:
        # Check if current inning is final inning and chasing team has surpassed the target score
        if self._is_final_innings(match):
            # Check if chasing team has surpassed the target score
            if match.get_current_inning().get_score() >= match.get_previous_inning().get_score() + 1:
                self.declare_winner(match, match.get_current_inning().get_batting_team())
                return
            # Check for all out
            elif self._is_all_out(match):
                self.declare_winner(match, match.get_current_inning().get_bowling_team())
                return
            # Check if all over finished
            elif self._are_overs_finished(match):
                # Check if chasing team has not surpassed the target score
                if match.get_current_inning().get_score() < match.get_previous_inning().get_score():
                    self.declare_winner(match, match.get_current_inning().get_bowling_team())
                # Check for a tie
                elif match.get_current_inning().get_score() == match.get_previous_inning().get_score():
                    self.declare_tie(match)
                return
        else:
            # Not final innings - check if current innings should end
            if self._is_all_out(match) or self._are_overs_finished(match):
                # End current innings and go to break
                match.set_status(MatchStatus.IN_BREAK)
                match.set_state(InBreakState())
                match.notify_observers(match, None)
                return

    def declare_tie(self, match: "Match"):
        print("MATCH TIE!")
        match.set_winner(None)
        match.update_player_statistics()
        match.set_status(MatchStatus.FINISHED)
        match.set_result_message(f"Match Tied between teams {match.get_team1().get_name()} and {match.get_team2().get_name()}")
        match.set_state(FinishedState())

    def declare_winner(self, match: "Match", winning_team: Team):
        print("MATCH FINISHED!")
        match.set_winner(winning_team)
        match.update_player_statistics()

        # Calculate the correct margin based on who won
        if winning_team == match.get_current_inning().get_batting_team():
            # Batting team won (chased the target) - show wickets remaining
            wickets_remaining = len(match.get_current_inning().get_batting_team().get_players()) - 1 - match.get_current_inning().get_wickets()
            result_message = f"{winning_team.get_name()} won by {wickets_remaining} wickets"
        else:
            # Bowling team won (defended the target) - show runs margin
            margin = match.get_previous_inning().get_score() - match.get_current_inning().get_score()
            result_message = f"{winning_team.get_name()} won by {margin} runs"

        print(f"DEBUG: Setting result message: {result_message}")
        match.set_result_message(result_message)
        match.set_status(MatchStatus.FINISHED)
        match.set_state(FinishedState())

    def start_next_inning(self, match: "Match"):
        print("ERROR: Cannot start the next innings from the live state.")


class InBreakState(MatchState):
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        print("ERROR: Cannot process a ball. The match is currently in a break.")

    def start_next_inning(self, match: "Match"):
        print("Starting the next innings...")
        match.create_new_inning(match.get_team2(), match.get_team1())
        match.set_state(LiveState())
        match.set_status(MatchStatus.LIVE)


class FinishedState(MatchState):
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        print("ERROR: Cannot process a ball. The match is finished.")

    def start_next_inning(self, match: "Match"):
        print("ERROR: Cannot start the next innings. The match is finished.")


class AbandonedState(MatchState):
    def process_ball(self, match: "Match", ball: Optional[Ball]):
        print("ERROR: Cannot process a ball. The match is abandoned.")

    def start_next_inning(self, match: "Match"):
        print("ERROR: Cannot start the next innings. The match is abandoned.")
