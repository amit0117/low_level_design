from app.models.board import Board
from app.models.player import Player
from app.models.enums import GameStatus
from app.observers.game_observer import GameSubject
from app.state.game_state import NotStartedState, GameState
from uuid import uuid4
from typing import Optional
from app.models.dice import Dice
from app.models.cell import Cell
import time


class Game(GameSubject):
    def __init__(self, board: Board, players: list[Player]) -> None:
        super().__init__()
        self.id = str(uuid4())
        self.winner: Optional[Player] = None
        self.board = board
        self.dice = Dice()
        self.status = GameStatus.NOT_STARTED
        self.players = players
        self.state: GameState = NotStartedState()
        self.current_player_index: int = 0
        self.max_self_play_count: int = 3
        # Add all players as observers
        for player in self.players:
            self.add_observer(player)

    def get_id(self) -> str:
        return self.id

    def get_players(self) -> list[Player]:
        return self.players

    def get_current_player(self) -> Optional[Player]:
        return self.players[self.current_player_index]

    def set_current_player_index(self, index: int) -> None:
        self.current_player_index = index

    def get_status(self) -> GameStatus:
        return self.status

    def get_state(self) -> GameState:
        return self.state

    def setStatus(self, status: GameStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def setState(self, state: GameState) -> None:
        self.state = state

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def declare_winner(self, winner: Player) -> None:
        self.winner = winner
        self.notify_observers(self)

    def add_player(self, player: Player) -> None:
        self.observers.append(player)
        self.players.append(player)
        player.add_game(self)

    def remove_player(self, player: Player) -> None:
        self.observers.remove(player)
        self.players.remove(player)
        player.remove_game(self)

    def play(self) -> None:
        self.state.play(self)

    def pause(self) -> None:
        self.state.pause(self)

    def resume(self) -> None:
        self.state.resume(self)

    def stop(self) -> None:
        self.state.stop(self)

    def make_move(self, self_play_count: int = 0) -> None:
        current_player = self.get_current_player()
        roll = self.dice.roll()
        next_position = self.calculate_next_position(current_player, roll)
        if next_position:
            current_player.set_current_position(next_position)
            if next_position.get_pos() == self.board.get_size() - 1:
                self.declare_winner(current_player)
                self.stop()  # Stop the game after declaring the winner
                return

            # if the player rolled a max value(6), they get another turn
            if roll == self.dice.get_max_value():
                self_play_count += 1
                if self_play_count < self.max_self_play_count:
                    print(f"{current_player.get_name()} rolled a {roll} and gets another turn!. Total consecutive turns: {self_play_count}")
                    self.make_move(self_play_count)
                else:
                    print(f"Max self play count reached. Turn skipped for {current_player.get_name()}. Turn passed to next player.")
                    self.set_current_player_index((self.current_player_index + 1) % len(self.get_players()))
            else:
                self.set_current_player_index((self.current_player_index + 1) % len(self.get_players()))
        else:
            print(
                f"{current_player.get_name()} needs {self.board.get_size() - current_player.get_current_position().get_pos()} to land exactly on {self.board.get_size() - 1} to win. Turn skipped."
            )
            self.set_current_player_index((self.current_player_index + 1) % len(self.get_players()))

    def calculate_next_position(self, player: Player, roll: int) -> Optional[Cell]:
        # sleep for 0.5 second to simulate the turn and dice roll
        time.sleep(0.5)

        print(f"{player.get_name()} rolled a {roll}\n")
        current_position = player.get_current_position()
        if self.board.is_cell_valid(Cell(current_position.get_pos() + roll)):
            next_position = Cell(current_position.get_pos() + roll)
            final_position = self.board.get_final_position(next_position)
            if final_position > next_position:
                print(f"{player.get_name()} found a ladder at {next_position.get_pos()} and climbed to {final_position.get_pos()}")
            elif final_position < next_position:
                print(f"{player.get_name()} was bitten by a snake at {next_position.get_pos()} and slid down to {final_position.get_pos()}")
            else:
                print(f"{player.get_name()} moved from {current_position.get_pos()} to {final_position.get_pos()}")
            return final_position
        else:
            return None
