from app.models.bank_server import BankServer
from threading import Lock


class BankRepository:
    _instance: "BankRepository" = None
    _lock: Lock = Lock()

    def __new__(cls) -> "BankRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "banks"):
            return
        self.banks: dict[str, BankServer] = dict()

    @classmethod
    def get_instance(cls) -> "BankRepository":
        return cls._instance or cls()

    def add_bank_server(self, bank_name: str, bank_server: BankServer) -> None:
        self.banks[bank_name] = bank_server

    def get_bank_server(self, bank_name: str) -> BankServer:
        return self.banks[bank_name]

    def get_all_banks(self) -> list[str]:
        return list(self.banks.keys())
