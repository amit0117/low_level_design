from app.models.stock_observer import StockSubject


class Stock:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price
        self.stock_subject: StockSubject = StockSubject()

    def get_price(self) -> float:
        return self.price

    def get_symbol(self) -> str:
        return self.symbol

    def set_price(self, new_price: float):
        # When price changes we should check if there is any Stop Loss/ Stop Limit order which has placed but
        if self.price != new_price:
            self.price = new_price
            self.stock_subject.notify_observers(self)
