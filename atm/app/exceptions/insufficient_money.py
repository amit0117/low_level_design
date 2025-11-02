class InsufficientCashException(Exception):  # Raised when the ATM does not have enough cash to dispense
    def __init__(self, message="Insufficient cash in the ATM"):
        super().__init__(message)


class InsufficientFundsException(Exception):  # Raised when the account does not have enough funds to withdraw
    def __init__(self, message="Insufficient funds in the account"):
        super().__init__(message)
