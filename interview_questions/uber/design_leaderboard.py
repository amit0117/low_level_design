# Design a leaderboard
# Functional Requirements:
# a) addScore(playerId,scrore)-> update the leaderboard by adding scrore to the given player's scrore.
# if there is no player with such id then add them to the leaderboard with given scrore
# b) top(k) -> return the sum of top k player (top k means top by scores)
# c) reset(playerId)-> reset the scrore with given id to 0 [it's guranteed that the player was added to the leaderboard before calling this function]

# Entity: player -> has score, leaderboard -> has players
# Data Structure Needed:-> In C++, we can't use map with custom comparator on value so that map remain sorted based on the values
# because when we update any value ,map doesn't update it's structure will only update when it's key. So using custom comparator on values, will not make our map strucure correct
# So we need to use map for the score of player and multiset for the sorting of the scores

# Similar will happen for Python, can't use list as for top(k) query we need to sort to get the correct answer
# so we need to use sortedlist (why sorted list and not sortedset because there might be some duplicate in the top values)

from __future__ import annotations
from sortedcontainers import SortedList

class Palyer:
    def __init__(self, player_id: int, name: str, score: int):
        self.player_id = player_id
        self.name = name
        self.score = score


class LeaderBoard:
    def __init__(self):
        self.leaderboard_scores = SortedList()
        self.players_score: dict[int, int] = dict()

    def add_score(self, player_id: int, score: int):
        if player_id not in self.players_score:
            self.players_score[player_id] = score
            self.leaderboard_scores.add(score)
        else:
            # first remove the old score of this playerid from the leaderboard_scores and then re-add
            self.leaderboard_scores.discard(
                self.players_score[player_id]
            )  # in this case we can use remove as well because we have already checked that player_id will always be present.
            # update the score int the players_score and add to the leaderboard_scores
            self.players_score[player_id] += score
            self.leaderboard_scores.add(self.players_score[player_id])

    def top(self, k: int) -> int:
        return sum(self.leaderboard_scores[-k:])

    def reset(self, player_id: int) -> None:
        old_score = self.players_score.pop(player_id, 0)
        self.leaderboard_scores.remove(old_score)


if __name__ == "__main__":
    lb = LeaderBoard()

    lb.add_score(1, 50)
    lb.add_score(2, 30)
    lb.add_score(3, 40)
    print("expected=90, actual=", lb.top(2))

    lb.add_score(2, 50)
    print("expected=130, actual=", lb.top(2))

    lb.add_score(4, 80)
    print("expected=210, actual=", lb.top(3))

    lb.reset(2)
    print("expected=130, actual=", lb.top(2))

    print("expected=170, actual=", lb.top(4))

    lb.add_score(2, 60)
    print("expected=140, actual=", lb.top(2))

    lb.reset(1)
    lb.reset(3)
    print("expected=140, actual=", lb.top(3))

    lb.reset(2)
    lb.reset(4)
    print("expected=0, actual=", lb.top(4))
