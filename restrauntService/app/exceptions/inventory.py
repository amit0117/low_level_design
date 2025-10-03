class OutOfStockException(Exception):
    def __init__(self, item_name: str) -> None:
        message = f"Item {item_name} is out of stock"
        super().__init__(message)


class InsufficientStockException(Exception):
    def __init__(self, item_name: str, required_quantity: int, present_quantity: int) -> None:
        message = f"Item {item_name} is insufficient stock. Required: {required_quantity}, Present: {present_quantity}"
        super().__init__(message)

