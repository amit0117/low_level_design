from app.models.cell import Cell


class Ladder:
    def __init__(self, start: Cell, end: Cell) -> None:
        self.start = start
        self.end = end

    def get_start_cell(self) -> Cell:
        return self.start

    def get_end_cell(self) -> Cell:
        return self.end
