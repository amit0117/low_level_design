from app.models.board import Board
from app.models.cell import Cell


class BoardService:
    def __init__(self) -> None:
        self.boards: list[Board] = []

    def create_board(self, size: int) -> Board:
        board = Board(size)
        self._setup_snakes_and_ladders(board)
        self.boards.append(board)
        return board

    def _setup_snakes_and_ladders(self, board: Board) -> None:
        """Setup predefined snakes and ladders on the board"""
        # Add snakes (head -> tail)
        snakes = [
            (17, 7),  # Snake from 17 to 7
            (54, 34),  # Snake from 54 to 34
            (62, 19),  # Snake from 62 to 19
            (98, 79),  # Snake from 98 to 79
        ]

        # Add ladders (bottom -> top)
        ladders = [
            (3, 38),  # Ladder from 3 to 38
            (24, 33),  # Ladder from 24 to 33
            (42, 93),  # Ladder from 42 to 93
            (72, 84),  # Ladder from 72 to 84
        ]

        # Add snakes to board (only if they fit on the board)
        snakes_added = 0
        for start, end in snakes:
            if start < board.get_size() and end < board.get_size():
                board.add_snake(Cell(start), Cell(end))
                snakes_added += 1

        # Add ladders to board (only if they fit on the board)
        ladders_added = 0
        for start, end in ladders:
            if start < board.get_size() and end < board.get_size():
                board.add_ladder(Cell(start), Cell(end))
                ladders_added += 1

        print(f"🎲 Board setup complete with {snakes_added} snakes and {ladders_added} ladders")

    def get_board_by_id(self, board_id: str) -> Board:
        for board in self.boards:
            if board.get_id() == board_id:
                return board
        raise ValueError(f"Board with id {board_id} not found")

    def get_all_boards(self) -> list[Board]:
        return self.boards
