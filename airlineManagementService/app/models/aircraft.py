class Aircraft:
    def __init__(self, model: str, total_seats: int, tail_number: str):
        self.model = model
        self.total_seats = total_seats
        self.tail_number = tail_number  # unique identifier for the aircraft which is used to identify the aircraft

    def get_model(self) -> str:
        return self.model

    def get_total_seats(self) -> int:
        return self.total_seats

    def get_tail_number(self) -> str:
        return self.tail_number
