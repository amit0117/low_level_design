from threading import Lock
from typing import Type
from app.models.gate import EntryGate, ExitGate


class GateRepository:
    _lock = Lock()
    _instance: "GateRepository" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "gates"):
            return
        self.entry_gates: dict[int, EntryGate] = dict()
        self.exit_gates: dict[int, ExitGate] = dict()

    @classmethod
    def get_instance(cls: Type["GateRepository"]) -> "GateRepository":
        return cls._instance or cls()

    def add_entry_gate(self, gate: EntryGate) -> None:
        self.entry_gates[gate.get_gate_number()] = gate

    def add_exit_gate(self, gate: ExitGate) -> None:
        self.exit_gates[gate.get_gate_number()] = gate

    def get_entry_gates(self) -> list[EntryGate]:
        return list(self.entry_gates.values())

    def get_exit_gates(self) -> list[ExitGate]:
        return list(self.exit_gates.values())

    def get_entry_gate(self, gate_number: int) -> EntryGate:
        return self.entry_gates.get(gate_number)

    def get_exit_gate(self, gate_number: int) -> ExitGate:
        return self.exit_gates.get(gate_number)
