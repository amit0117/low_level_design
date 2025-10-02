from app.models.enums import WicketType
from app.models.player import Player
from typing import Optional
from uuid import uuid4


class Wicket:
    def __init__(
        self,
        wicket_type: WicketType,
        out_player: Player,
        caught_by: Optional[Player],
        runout_by: Optional[Player],
        bowled_by: Optional[Player],
        lbw_by: Optional[Player],
        stumped_by: Optional[Player],
        hit_wicket_by: Optional[Player],
    ):
        self.id = str(uuid4())
        self.wicket_type = wicket_type
        self.out_player = out_player
        self.caught_by = caught_by
        self.runout_by = runout_by
        self.bowled_by = bowled_by
        self.lbw_by = lbw_by
        self.stumped_by = stumped_by
        self.hit_wicket_by = hit_wicket_by

    def get_id(self) -> str:
        return self.id

    def get_out_player(self) -> Player:
        return self.out_player

    def get_caught_by(self) -> Optional[Player]:
        return self.caught_by

    def get_runout_by(self) -> Optional[Player]:
        return self.runout_by

    def get_bowled_by(self) -> Optional[Player]:
        return self.bowled_by

    def get_lbw_by(self) -> Optional[Player]:
        return self.lbw_by

    def get_stumped_by(self) -> Optional[Player]:
        return self.stumped_by

    def get_hit_wicket_by(self) -> Optional[Player]:
        return self.hit_wicket_by

    def get_wicket_type(self) -> WicketType:
        return self.wicket_type
