class Ingredient:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity

    def get_name(self) -> str:
        return self.name

    def get_quantity(self) -> int:
        return self.quantity

    def update_quantity(self, amount: int) -> None:
        self.quantity += amount
