import random


class Dice:
    def __init__(self, min_value: int = 1, max_value: int = 6) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def roll(self) -> int:
        return random.randint(self.min_value, self.max_value)

    def get_max_value(self) -> int:
        return self.max_value
