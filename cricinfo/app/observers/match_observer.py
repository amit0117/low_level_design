from abc import ABC, abstractmethod
from app.models.ball import Ball
from app.models.enums import MatchStatus
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.match import Match


class MatchObserver(ABC):
    @abstractmethod
    def update(self, match: "Match", ball: Optional[Ball]):
        raise NotImplementedError("Subclasses must implement this method")


class ScorecardDisplay(MatchObserver):
    def update(self, match: "Match", ball: Optional[Ball]):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("\n--- MATCH RESULT ---")
            print(match.get_result_message().upper())
            print("--------------------")
            print("Player Stats:")
            counter = 1
            for inning in match.get_innings():
                print(f"Inning {counter}")
                counter += 1
                inning.print_player_stats()
            print("\n\n")
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("\n--- END OF INNINGS ---")
            last_inning = match.get_current_inning()
            print(
                f"Final Score of last inning: {last_inning.get_batting_team().get_name()}: {last_inning.get_score()}/{last_inning.get_wickets()} (Overs: {last_inning.get_overs_till_now():.1f})"
            )
            print("------------------------\n")
        else:
            print("\n--- SCORECARD UPDATE ---")
            current_inning = match.get_current_inning()
            print(
                f"Current Score: {current_inning.get_batting_team().get_name()}: {current_inning.get_score()}/{current_inning.get_wickets()} (Overs: {current_inning.get_overs_till_now():.1f})"
            )
            print("------------------------\n")


class UserNotifier(MatchObserver):
    def update(self, match: "Match", ball: Optional[Ball]):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("[NOTIFICATION]: Match has finished!")
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("[NOTIFICATION]: Inning has ended!")
        elif ball and ball.is_wicket():
            print("[NOTIFICATION]: Wicket! A player is out.")
        elif ball and ball.is_boundary():
            print(f"[NOTIFICATION]: It's a boundary! {ball.get_runs_scored()} runs.")


class CommentaryManager(MatchObserver):
    def update(self, match: "Match", ball: Optional[Ball]):
        if match.get_current_status() == MatchStatus.FINISHED:
            print("[COMMENTARY]: Match has finished!")
        elif match.get_current_status() == MatchStatus.IN_BREAK:
            print("[COMMENTARY]: Inning has ended!")
        elif ball:
            print(f"[COMMENTARY]: {ball.get_commentary()}")


class MatchSubject:
    def __init__(self):
        self.observers: list[MatchObserver] = []

    def add_observer(self, observer: MatchObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: MatchObserver):
        self.observers.remove(observer)

    def notify_observers(self, match: "Match", ball: Optional[Ball]):
        for observer in self.observers:
            observer.update(match, ball)
