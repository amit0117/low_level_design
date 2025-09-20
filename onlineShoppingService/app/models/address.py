class Address:
    def __init__(self, street: str, city: str, state: str, zip_code: str, country: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def get_street(self) -> str:
        return self.street

    def get_city(self) -> str:
        return self.city

    def get_state(self) -> str:
        return self.state

    def get_zip_code(self) -> str:
        return self.zip_code

    def set_street(self, street: str) -> None:
        self.street = street

    def set_city(self, city: str) -> None:
        self.city = city

    def set_state(self, state: str) -> None:
        self.state = state

    def set_zip_code(self, zip_code: str) -> None:
        self.zip_code = zip_code

    def __repr__(self) -> str:
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"
