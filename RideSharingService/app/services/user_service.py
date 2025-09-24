from app.models.user import User
from typing import Optional
from app.models.enums import UserType
from app.models.rider import Rider
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.location import Location


# This will handle both Rider and Driver
class UserService:
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def add_rider(self, name: str, email: str) -> Rider:
        rider = Rider(name, email)
        self.users[rider.get_id()] = rider
        return rider

    def remove_rider(self, id: str) -> None:
        if id not in self.users:
            print(f"Rider with id {id} not found")
            return
        del self.users[id]

    def add_driver(self, name: str, email: str, vehicle: Vehicle, location: Location) -> Driver:
        driver = Driver(name, email, vehicle, location)
        self.users[driver.get_id()] = driver
        return driver

    def remove_driver(self, id: str) -> None:
        if id not in self.users:
            print(f"Driver with id {id} not found")
            return
        del self.users[id]

    def does_user_exist(self, id: str) -> bool:
        return id in self.users

    def get_user_by_id(self, id: str) -> Optional[User]:
        if id not in self.users:
            print(f"User with id {id} not found")
            return None
        return self.users.get(id)

    def get_user_by_name(self, name: str) -> list[User]:
        return [user for user in self.users.values() if user.get_name().lower() == name.lower()]

    def all_drivers(self) -> list[User]:
        return [user for user in self.users.values() if user.get_type() == UserType.DRIVER]

    def all_riders(self) -> list[User]:
        return [user for user in self.users.values() if user.get_type() == UserType.RIDER]
