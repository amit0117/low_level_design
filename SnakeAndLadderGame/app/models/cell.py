class Cell:
    def __init__(self, pos: int):
        self.pos = pos

    def get_pos(self) -> int:
        return self.pos

    def set_pos(self, pos: int) -> None:
        self.pos = pos

    def __lt__(self, other):
        return self.pos < other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)

    def __repr__(self):
        return f"Cell({self.pos})"
