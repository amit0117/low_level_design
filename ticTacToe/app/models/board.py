from app.models.enums import PlayerSymbol
import random
from typing import Optional


class Board:
    def __init__(self, size: int = 3) -> None:
        self.board = [["-" for _ in range(size)] for _ in range(size)]

    def is_cell_valid(self, row: int, col: int) -> bool:
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])

    def is_full(self) -> bool:
        return all(cell != "-" for row in self.board for cell in row)

    def make_move(self, row: int, col: int, symbol: PlayerSymbol) -> bool:
        if self.is_full() or not self.is_cell_valid(row, col) or self.board[row][col] != "-":
            return False
        self.board[row][col] = symbol.value  # Store the string value
        return True

    def get_available_cells(self) -> list[tuple[int, int]]:
        return [(row, col) for row in range(len(self.board)) for col in range(len(self.board[0])) if self.board[row][col] == "-"]

    def get_random_available_cell(self) -> Optional[tuple[int, int]]:
        if self.is_full():
            return None
        available_cells = self.get_available_cells()
        return random.choice(available_cells)

    def get_board(self) -> list[list[str]]:
        """Get the current board state"""
        return self.board
