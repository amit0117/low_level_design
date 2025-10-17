from uuid import uuid4
from app.models.enums import AuctionItemType


class AuctionItem:
    def __init__(self, name: str, description: str, starting_price: float, item_type: AuctionItemType):
        self.id = str(uuid4())
        self.name = name
        self.description = description
        self.starting_price = starting_price
        self.item_type = item_type

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_starting_price(self) -> float:
        return self.starting_price

    def get_item_type(self) -> AuctionItemType:
        return self.item_type
