import getpass


class Keypad:
    def __init__(self):
        self.pin = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pin = None

    def enter_pin(
        self,
    ) -> None:
        # take input from the user
        pin = getpass.getpass("Enter your PIN: ")
        self.pin = pin

    def get_pin(self) -> str:
        return self.pin
