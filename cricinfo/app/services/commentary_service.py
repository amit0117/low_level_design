import random
from app.models.ball import Ball
from app.models.enums import WicketType, ExtraType


class CommentaryService:

    def __init__(self) -> None:
        self.initialize_templates()

    def initialize_templates(self) -> None:
        self.commentary_templates = {
            "RUNS": {
                0: [
                    "{batsman} defends solidly.",
                    "No run, good fielding by the cover fielder.",
                    "A dot ball to end the over.",
                    "Pushed to mid-on, but no run.",
                ],
                1: ["Tucked away to the leg side for a single.", "Quick single taken by {batsman}.", "Pushed to long-on for one."],
                2: ["Two runs taken!", "Quick double taken by {batsman}.", "Pushed to mid-on for two."],
                4: ["FOUR! {batsman} smashes it through the covers!", "Beautiful shot! That's a boundary.", "Finds the gap perfectly. Four runs."],
                6: ["SIX! That's out of the park!", "{batsman} sends it sailing over the ropes!", "Massive hit! It's a maximum."],
            },
            "WICKET": {
                WicketType.BOWLED.value: [
                    "BOWLED HIM! {batsman} misses completely and the stumps are shattered!",
                    "Cleaned up! A perfect yorker from {bowler}.",
                ],
                WicketType.CAUGHT.value: [
                    "CAUGHT! {batsman} skies it and the fielder takes a comfortable catch.",
                    "Out! A brilliant catch in the deep by {bowler}.",
                ],
                WicketType.LBW.value: [
                    "LBW! That one kept low and struck {batsman} right in front.",
                    "{batsman} completely misjudged the line and pays the price.",
                ],
                WicketType.STUMPED.value: [
                    "STUMPED! {batsman} misses it, and the keeper does the rest!",
                    "Gone! Lightning-fast work by the keeper to stump {batsman}.",
                ],
                WicketType.RUN_OUT.value: [
                    "RUN OUT! {batsman} is out!",
                    "Out! {batsman} is out!",
                ],
                WicketType.HIT_WICKET.value: [
                    "HIT WICKET! {batsman} is hit on the hand and is out!",
                    "Out! {batsman} is hit on the hand and is out!",
                ],
            },
            "EXTRA": {
                ExtraType.WIDE.value: ["That's a wide. The umpire signals an extra run.", "Too far down the leg side, that'll be a wide."],
                ExtraType.NO_BALL.value: ["No ball! {bowler} has overstepped. It's a free hit.", "It's a no-ball for overstepping."],
                ExtraType.BYE.value: ["That's a bye. The umpire signals an extra run.", "Too far down the leg side, that'll be a bye."],
                ExtraType.LEG_BYE.value: ["That's a leg bye. The umpire signals an extra run.", "Too far down the leg side, that'll be a leg bye."],
            },
        }

    def generate_commentary(self, ball: Ball):
        batsman = ball.get_faced_by().get_name() if ball.get_faced_by() else ""
        bowler = ball.get_bowled_by().get_name() if ball.get_bowled_by() else ""

        key, sub_key = self.get_event_key(ball)
        if not key or not sub_key:
            print("ERROR: No key or subkey found for the ball.")
            return ""
        templates = self.commentary_templates.get(key, {}).get(sub_key, ["Just a standard delivery."])
        template = random.choice(templates)

        return template.format(batsman=batsman, bowler=bowler)

    @staticmethod
    def get_event_key(ball: Ball):
        if ball.is_wicket():
            return "WICKET", ball.get_wicket_type().value
        elif ball.get_extra_type():
            return "EXTRA", ball.get_extra_type().value
        elif 0 <= ball.get_runs_scored() <= 6:
            return "RUNS", ball.get_runs_scored()
        return None, None
