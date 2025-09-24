from uuid import uuid4
from app.models.enums import UserType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ride import Ride


class User:
    def __init__(self, name: str, contact: str, type: UserType = UserType.RIDER):
        self.id = str(uuid4())
        self.name = name
        self.contact = contact
        self.ride_history: list["Ride"] = []
        self.type = type

    def add_ride_to_history(self, ride: "Ride"):
        self.ride_history.append(ride)

    def get_ride_history(self) -> list["Ride"]:
        return self.ride_history

    def get_name(self) -> str:
        return self.name

    def get_contact(self) -> str:
        return self.contact

    def get_id(self) -> str:
        return self.id

    def get_type(self) -> UserType:
        return self.type
