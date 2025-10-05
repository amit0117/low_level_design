from threading import Lock
from typing import Optional
from app.models.member import Member


class MemberRepository:
    _lock = Lock()
    _instance: "MemberRepository" = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "members"):
            return
        self.process_lock = Lock()
        self.members: list[Member] = []

    @classmethod
    def get_instance(cls) -> "MemberRepository":
        return cls._instance or cls()

    def add_member(self, member: Member):
        with self.process_lock:
            self.members.append(member)

    def remove_member(self, member: Member):
        with self.process_lock:
            if not self.get_member_by_id(member.get_id()):
                raise ValueError("Member not found")
            self.members.remove(member)

    def get_member_by_id(self, id: str) -> Optional[Member]:
        return next((member for member in self.members if member.get_id() == id), None)

    def get_member_by_name(self, name: str) -> Optional[Member]:
        return next((member for member in self.members if member.get_name().lower() == name.lower()), None)

    def get_all_members(self) -> list[Member]:
        return self.members
