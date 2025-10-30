from app.models.player import Player
from app.models.board import Board
from app.models.enums import GameStatus
from app.states.game_state import GameState, NotStartedState
from typing import Optional
from app.observers.game_observer import GameSubject
from uuid import uuid4


class Game(GameSubject):
    def __init__(self, players: list[Player], board: Board, consecutive_moves_to_win: int = 3) -> None:
        super().__init__()
        self.id = str(uuid4())
        self.players = players
        self.board = board
        self.status = GameStatus.NOT_STARTED
        self.state: GameState = NotStartedState()
        self.current_player_index: int = 0
        self.winner: Optional[Player] = None
        self.consecutive_moves_to_win = consecutive_moves_to_win
        # keep map for dict for each row , col, diagonal and anti-diagonal, count the number of consecutive moves
        # TODO: if k==n like 3x3, then we can determine the winner by checking the number of consecutive moves in a row, col, diagonal and anti-diagonal (O(1) time complexity)
        # eg , for each player we keep track of the number of consecutive moves in a row, col, diagonal and anti-diagonal

        # But if k!=n, then on each move we need to check the number of consecutive moves in a row, col, diagonal and anti-diagonal for each player (O(4(2*k) = O(8k) time complexity)
        # 4 -> for each of the 4 directions (row, col, diagonal, anti-diagonal)
        # for each direction we will check from the current cell to k cell up/down/left/right

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_next_player(self) -> Player:
        return self.players[(self.current_player_index + 1) % len(self.players)]

    def get_board(self) -> Board:
        return self.board

    def get_status(self) -> GameStatus:
        return self.status

    def get_state(self) -> GameState:
        return self.state

    def get_current_player_index(self) -> int:
        return self.current_player_index

    def get_players(self) -> list[Player]:
        return self.players

    def set_state(self, state: GameState) -> None:
        self.state = state

    def set_status(self, status: GameStatus) -> None:
        self.status = status
        self.notify_observers(self)

    def get_winner(self) -> Optional[Player]:
        return self.state.get_winner(self)

    def set_winner(self, winner: Player) -> None:
        print(f"Game with id {self.id} is finished. Winner is {winner.get_name()}\n\n")
        self.winner = winner

    def start(self) -> None:
        self.state.start(self)

    def make_move(self) -> None:
        self.state.make_move(self)

    def end(self) -> None:
        self.state.end(self)

    def check_winner(self, player: Player, row: int, col: int) -> bool:
        board = self.get_board().get_board()
        symbol = player.get_symbol().value

        # Check for consecutive moves in a row(horizontal)
        consecutive_moves_count = 0
        for i in range(max(0, row - self.consecutive_moves_to_win + 1), min(row + self.consecutive_moves_to_win, len(board[0]))):
            if board[i][col] == symbol:
                consecutive_moves_count += 1
            else:
                consecutive_moves_count = 0
            if consecutive_moves_count == self.consecutive_moves_to_win:
                return True

        # Check for consecutive moves in a column(vertical)
        consecutive_moves_count = 0
        for i in range(max(0, col - self.consecutive_moves_to_win + 1), min(col + self.consecutive_moves_to_win, len(board))):
            if board[row][i] == symbol:
                consecutive_moves_count += 1
            else:
                consecutive_moves_count = 0
            if consecutive_moves_count == self.consecutive_moves_to_win:
                return True

        # Check for consecutive moves in a diagonal(top-left to bottom-right)
        consecutive_moves_count = 0
        top_left = row, col
        i, j = (row, col)
        while self.get_board().is_cell_valid(i, j):
            top_left = (i, j)
            i -= 1
            j -= 1

        # move from top_left to bottom_right
        i, j = top_left
        consecutive_moves_count = 0
        while self.get_board().is_cell_valid(i, j):
            if board[i][j] == symbol:
                consecutive_moves_count += 1
            else:
                consecutive_moves_count = 0
            if consecutive_moves_count == self.consecutive_moves_to_win:
                return True
            i += 1
            j += 1

        # Check for consecutive moves in an anti-diagonal(bottom-left to top-right)
        consecutive_moves_count = 0
        bottom_left = row, col
        i, j = (row, col)
        while self.get_board().is_cell_valid(i, j):
            bottom_left = (i, j)
            i += 1
            j -= 1

        # move from bottom_left to top_right
        i, j = bottom_left
        consecutive_moves_count = 0
        while self.get_board().is_cell_valid(i, j):
            if board[i][j] == symbol:
                consecutive_moves_count += 1
            else:
                consecutive_moves_count = 0
            if consecutive_moves_count == self.consecutive_moves_to_win:
                return True
            i -= 1
            j += 1

        return False

    def check_for_draw(self) -> bool:
        return self.get_board().is_full() and not self.get_winner()
