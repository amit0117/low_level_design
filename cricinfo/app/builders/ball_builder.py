from app.models.ball import Ball
from app.models.enums import ExtraType
from app.models.wicket import Wicket
from app.models.player import Player
from app.services.commentary_service import CommentaryService


class BallBuilder:
    def __init__(self):
        self.ball_number = None
        self.bowled_by = None
        self.faced_by = None
        self.runs_scored = None
        self.wicket = None
        self.extra_type = None
        self.commentary = None
        self.commentary_service = CommentaryService()

    def with_ball_number(self, ball_number: int) -> "BallBuilder":
        self.ball_number = ball_number
        return self

    def with_bowled_by(self, bowled_by: Player) -> "BallBuilder":
        self.bowled_by = bowled_by
        return self

    def with_faced_by(self, faced_by: Player) -> "BallBuilder":
        self.faced_by = faced_by
        return self

    def with_runs_scored(self, runs_scored: int) -> "BallBuilder":
        self.runs_scored = runs_scored
        return self

    def with_wicket(self, wicket: Wicket) -> "BallBuilder":
        self.wicket = wicket
        return self

    def with_extra_type(self, extra_type: ExtraType) -> "BallBuilder":
        self.extra_type = extra_type
        return self

    def with_commentary(self, commentary: str) -> "BallBuilder":
        self.commentary = commentary
        return self

    def validate(self) -> None:
        if self.ball_number is None or self.bowled_by is None or self.faced_by is None or self.runs_scored is None:
            raise ValueError("Missing mandatory fields to build Ball")
        if self.wicket and self.extra_type:
            raise ValueError("Wicket and extra type cannot be set at the same time.")

    def build(self) -> Ball:
        self.validate()

        # Create a temporary ball to generate commentary
        temp_ball = Ball(
            self.ball_number,
            self.bowled_by,
            self.faced_by,
            self.runs_scored,
            self.wicket,
            self.extra_type,
            self.commentary or "",  # Use provided commentary or empty string
        )

        # Generate automatic commentary if none provided
        if not self.commentary:
            self.commentary = self.commentary_service.generate_commentary(temp_ball)

        return Ball(self.ball_number, self.bowled_by, self.faced_by, self.runs_scored, self.wicket, self.extra_type, self.commentary)
