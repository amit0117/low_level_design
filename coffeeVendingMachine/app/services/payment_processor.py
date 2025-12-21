from app.models.enums import Coin
from threading import Lock


class PaymentProcessor:
    def __init__(self):
        self.lock = Lock()

    def process_payment(self, price: float, coins: list[Coin]) -> tuple[bool, float]:
        with self.lock:
            total = sum(coin.value for coin in coins)
            if total >= price:
                return True, total
            return False, total

    def calculate_change(self, paid: float, price: float) -> float:
        return max(0, paid - price)
