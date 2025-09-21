import uuid
from app.models.screen import Screen
from app.models.show import Show


class Cinema:
    def __init__(self, name: str, city: str, screens: list[Screen]):
        self._id = str(uuid.uuid4())
        self._name = name
        self._city = city
        self._screens = screens

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def city(self) -> str:
        return self._city

    @property
    def screens(self) -> list[Screen]:
        return self._screens

    def get_screens(self) -> list[Screen]:
        return self._screens

    def add_screen(self, screen: Screen) -> None:
        self._screens.append(screen)
