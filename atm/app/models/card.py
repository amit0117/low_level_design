from datetime import datetime


class Card:
    def __init__(self, card_number: str, cvv: str, expiration_date: datetime):  # CVV:- Card Verification Value, 3 digits
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date

    def get_card_number(self) -> str:
        return self.card_number

    def get_cvv(self) -> str:
        return self.cvv

    def get_expiration_date(self) -> datetime:
        return self.expiration_date
