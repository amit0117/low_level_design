class MissingItemException(Exception):
    def __init__(self, item_name: str) -> None:
        message = f"Item {item_name} is missing"
        super().__init__(message)
