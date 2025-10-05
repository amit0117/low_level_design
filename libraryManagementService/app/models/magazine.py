from app.models.library_item import LibraryItem
from app.models.enums import ItemType


class Magazine(LibraryItem):
    def __init__(self, title: str, author: str, publication_year: int, issn: int):
        super().__init__(title, author, ItemType.MAGAZINE)
        self.publication_year = publication_year
        self.issn = issn  # International Standard Serial Number

    def get_publication_year(self) -> int:
        return self.publication_year

    def set_publication_year(self, publication_year: int):
        self.publication_year = publication_year

    def get_issn(self) -> int:
        return self.issn

    def set_issn(self, issn: int):
        self.issn = issn

    def display_info(self):
        super().display_info()
        print(f"Publication Year: {self.publication_year}")
        print(f"ISSN: {self.issn}")
