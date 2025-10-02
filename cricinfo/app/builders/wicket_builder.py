from app.models.enums import WicketType
from app.models.player import Player
from app.models.wicket import Wicket


class WicketBuilder:
    def __init__(self):
        self.wicket_type = None
        self.out_player = None
        self.caught_by = None
        self.runout_by = None
        self.bowled_by = None
        self.lbw_by = None
        self.stumped_by = None
        self.hit_wicket_by = None

    def with_wicket_type(self, wicket_type: WicketType) -> "WicketBuilder":
        self.wicket_type = wicket_type
        return self

    def with_out_player(self, out_player: Player) -> "WicketBuilder":
        self.out_player = out_player
        return self

    def with_caught_by(self, caught_by: Player) -> "WicketBuilder":
        self.caught_by = caught_by
        return self

    def with_runout_by(self, runout_by: Player) -> "WicketBuilder":
        self.runout_by = runout_by
        return self

    def with_bowled_by(self, bowled_by: Player) -> "WicketBuilder":
        self.bowled_by = bowled_by
        return self

    def with_lbw_by(self, lbw_by: Player) -> "WicketBuilder":
        self.lbw_by = lbw_by
        return self

    def with_stumped_by(self, stumped_by: Player) -> "WicketBuilder":
        self.stumped_by = stumped_by
        return self

    def with_hit_wicket_by(self, hit_wicket_by: Player) -> "WicketBuilder":
        self.hit_wicket_by = hit_wicket_by
        return self

    def validate(self) -> None:
        if not self.wicket_type or not self.out_player:
            raise ValueError("Wicket type and out player are required to build a wicket.")
        wicket_type_to_out_by_map = {
            WicketType.CAUGHT: self.caught_by,
            WicketType.RUN_OUT: self.runout_by,
            WicketType.LBW: self.lbw_by,
            WicketType.STUMPED: self.stumped_by,
            WicketType.HIT_WICKET: self.hit_wicket_by,
        }
        for wicket_type, out_by_player in wicket_type_to_out_by_map.items():
            if wicket_type == self.wicket_type and out_by_player is None:
                raise ValueError(f"{wicket_type} wicket type requires a {wicket_type} by player")

    def build(self) -> Wicket:
        self.validate()
        return Wicket(
            self.wicket_type, self.out_player, self.caught_by, self.runout_by, self.bowled_by, self.lbw_by, self.stumped_by, self.hit_wicket_by
        )
