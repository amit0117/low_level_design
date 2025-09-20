class OutOfStockException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientFundsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientStockException(Exception):
    def __init__(self, message):
        super().__init__(message)
