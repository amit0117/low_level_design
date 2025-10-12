class InsufficientFundsException(Exception):
    def __init__(self) -> None:
        message = "Insufficient funds to make the transaction"
        super().__init__(message)
