from app.models.player import Player
from app.models.enums import ExtraType, WicketType
from app.models.wicket import Wicket
from uuid import uuid4
from typing import Optional


class Ball:
    def __init__(
        self,
        ball_number: int,
        bowled_by: Player,
        faced_by: Player,
        runs_scored: Optional[int],
        wicket: Optional[Wicket],
        extra_type: Optional[ExtraType],
        commentary: str,
    ):
        self.id = str(uuid4())
        self.ball_number = ball_number
        self.bowled_by = bowled_by
        self.faced_by = faced_by
        self.runs_scored = runs_scored
        self.wicket = wicket
        self.extra_type = extra_type
        self.commentary = commentary

    def get_id(self) -> str:
        return self.id

    def get_ball_number(self) -> int:
        return self.ball_number

    def get_bowled_by(self) -> Player:
        return self.bowled_by

    def get_faced_by(self) -> Player:
        return self.faced_by

    def get_runs_scored(self) -> Optional[int]:
        return self.runs_scored or 0

    def is_wicket(self) -> bool:
        return self.wicket is not None

    def is_boundary(self) -> bool:
        return self.runs_scored in [4, 6]

    def get_commentary(self) -> str:
        return self.commentary

    def get_extra_type(self) -> Optional[ExtraType]:
        return self.extra_type

    def get_wicket_type(self) -> Optional[WicketType]:
        return self.wicket.get_wicket_type() if self.wicket else None

    def __str__(self) -> str:
        return f"Ball(id={self.id}, ball_number={self.ball_number}, bowled_by={self.bowled_by}, faced_by={self.faced_by}, runs_scored={self.runs_scored}, wicket={self.wicket}, extra_type={self.extra_type}, commentary={self.commentary})"
