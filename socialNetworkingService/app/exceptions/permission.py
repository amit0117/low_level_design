class PermissionError(Exception):
    def __init__(self, message: str = "You are not allowed to perform this action."):
        self.message = message
        super().__init__(self.message)
