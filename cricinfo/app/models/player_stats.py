from threading import Lock


class PlayerStats:
    def __init__(self):
        self.runs = 0
        self.balls_faced = 0
        self.wickets_taken = 0
        self.balls_bowled = 0
        self.matches_played = 0
        self.lock = Lock()

    def update_runs(self, runs: int) -> None:
        with self.lock:
            self.runs += runs

    def increment_balls_faced(self) -> None:
        with self.lock:
            self.balls_faced += 1

    def increment_wickets_taken(self) -> None:
        with self.lock:
            self.wickets_taken += 1

    def increment_balls_bowled(self) -> None:
        with self.lock:
            self.balls_bowled += 1

    def increment_matches_played(self) -> None:
        with self.lock:
            self.matches_played += 1

    def get_runs(self) -> int:
        return self.runs

    def get_balls_faced(self) -> int:
        return self.balls_faced

    def get_wickets_taken(self) -> int:
        return self.wickets_taken

    def get_balls_bowled(self) -> int:
        return self.balls_bowled

    def get_matches_played(self) -> int:
        return self.matches_played

    def __str__(self) -> str:
        return f"Runs: {self.runs}, Balls Faced: {self.balls_faced}, Wickets Taken: {self.wickets_taken}, Balls Bowled: {self.balls_bowled}, Matches Played: {self.matches_played}"
