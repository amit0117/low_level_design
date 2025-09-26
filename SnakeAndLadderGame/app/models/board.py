from app.models.cell import Cell
from uuid import uuid4


class Board:
    def __init__(self, size: int) -> None:
        self.id = str(uuid4())
        # Assuming the board is a 1D array and each cell is a square
        self.size = size
        self.cells: list[Cell] = [Cell(pos) for pos in range(size)]
        # snakes and ladders are represented as a dictionary of start cell and end cell
        self.snakes_and_ladders: dict[Cell, Cell] = {}

    def get_id(self) -> str:
        return self.id

    def get_size(self) -> int:
        return self.size

    def get_cells(self) -> list[Cell]:
        return self.cells

    def get_cell(self, cell: Cell) -> Cell:
        if not self.is_cell_valid(cell):
            raise ValueError("Invalid cell")
        return self.cells[cell.get_pos()]

    def get_final_position(self, cell: Cell) -> Cell:
        # if the cell is a snake or ladder, return the end cell else return the cell
        return self.snakes_and_ladders.get(cell, cell)

    def add_snake(self, start: Cell, end: Cell) -> None:
        if any(not self.is_cell_valid(cell) for cell in [start, end]):
            raise ValueError("Invalid start or end cell")
        # start is the head of the snake and end is the tail
        # When player lands on head (start), they slide down to tail (end)
        self.snakes_and_ladders[start] = end

    def add_ladder(self, start: Cell, end: Cell) -> None:
        if any(not self.is_cell_valid(cell) for cell in [start, end]):
            raise ValueError("Invalid start or end cell")
        # start is the bottom of the ladder and end is the top
        self.snakes_and_ladders[start] = end

    def is_cell_valid(self, cell: Cell) -> bool:
        return cell.get_pos() >= 0 and cell.get_pos() < self.size
