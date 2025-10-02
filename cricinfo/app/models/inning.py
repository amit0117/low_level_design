from app.models.player_stats import PlayerStats
from app.models.ball import Ball
from app.models.team import Team
from app.models.player import Player
from app.models.enums import ExtraType


class Inning:
    def __init__(self, batting_team: Team, bowling_team: Team):
        self.bowling_team = bowling_team
        self.batting_team = batting_team
        self.player_stats: dict[Player, PlayerStats] = {}
        self.ball: list[Ball] = []
        self.score = 0
        self.wickets = 0
        # Initialize player stats for each player in the bowling and batting team
        for player in bowling_team.get_players():
            self.player_stats[player] = PlayerStats()
        for player in batting_team.get_players():
            self.player_stats[player] = PlayerStats()

    def add_ball(self, ball: Ball):
        self.ball.append(ball)
        self.score += ball.get_runs_scored()

        # Update the global and innings stats of the bowler
        bowler = ball.get_bowled_by()
        self.bowling_team.find_player(bowler.get_id()).get_stats().increment_balls_bowled()
        self.player_stats[bowler].increment_balls_bowled()

        if ball.is_wicket():
            self.player_stats[bowler].increment_wickets_taken()
            self.bowling_team.find_player(bowler.get_id()).get_stats().increment_wickets_taken()
            self.wickets += 1
        elif ball.get_extra_type() in [ExtraType.WIDE, ExtraType.NO_BALL]:
            self.score += 1  # Extra runs are added to the Team's score
        else:
            # Update the global and innings stats of the batsman
            batsman = ball.get_faced_by()
            # Global stats
            self.batting_team.find_player(batsman.get_id()).get_stats().increment_balls_faced()
            self.batting_team.find_player(batsman.get_id()).get_stats().update_runs(ball.get_runs_scored())
            # Innings stats
            self.player_stats[batsman].increment_balls_faced()
            self.player_stats[batsman].update_runs(ball.get_runs_scored())

    def print_player_stats(self):
        print("Batting Team Stats:", self.batting_team.get_name(), ":\n")
        for player in self.batting_team.get_players():
            global_stats = player.get_stats()
            if global_stats.get_balls_faced() > 0 or global_stats.get_balls_bowled() > 0:
                print(f"Player: {player.get_name()} - Stats: {global_stats}")
        print("\n\n")
        print("Bowling Team Stats:", self.bowling_team.get_name(), ":\n")
        for player in self.bowling_team.get_players():
            global_stats = player.get_stats()
            if global_stats.get_balls_bowled() > 0 or global_stats.get_balls_faced() > 0:
                print(f"Player: {player.get_name()} - Stats: {global_stats}")
        print("\n")

    def get_score(self) -> int:
        return self.score

    def get_wickets(self) -> int:
        return self.wickets

    def get_balls(self) -> list[Ball]:
        return self.ball.copy()

    def get_batting_team(self) -> Team:
        return self.batting_team

    def get_bowling_team(self) -> Team:
        return self.bowling_team

    def get_player_stats(self) -> dict[Player, PlayerStats]:
        return self.player_stats

    def get_bowling_team_stats(self) -> dict[Player, PlayerStats]:
        return {player: stats for player, stats in self.player_stats.items() if player in self.bowling_team.get_players()}

    def get_batting_team_stats(self) -> dict[Player, PlayerStats]:
        return {player: stats for player, stats in self.player_stats.items() if player in self.batting_team.get_players()}

    def get_overs_till_now(self) -> float:
        # exclude wide and no balls to consider valid balls
        valid_balls = sum(1 for ball in self.ball if ball.get_extra_type() not in [ExtraType.WIDE, ExtraType.NO_BALL])
        completed_overs = valid_balls // 6
        balls_in_current_over = valid_balls % 6
        return completed_overs + (balls_in_current_over / 10.0)
