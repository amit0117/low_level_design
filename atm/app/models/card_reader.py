from app.models.card import Card


class CardReader:
    def __init__(self):
        self.card = None
    

    def read_card(self) -> Card:
        if self.card is None:
            raise ValueError("No card inserted")
        print(f"Card read: {self.card.get_card_number()} with CVV {self.card.get_cvv()} expiring on {self.card.get_expiration_date()}")
        return self.card

    def insert_card(self, card: Card) -> None:
        self.card = card

    def remove_card(self) -> None:
        self.card = None
