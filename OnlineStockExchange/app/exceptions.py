class InsufficientFundException(Exception):
    def __init__(self,message="Insufficient Fund in Account"):
        super().__init__(message)

class InsufficientStockException(Exception):
    def __init__(self,message="Insufficient Stock in Account"):
        super().__init__(message)


class NoMatchStockFoundException(Exception):
    def __init__(self, message="No matched stock found"):
        super().__init__(message)
