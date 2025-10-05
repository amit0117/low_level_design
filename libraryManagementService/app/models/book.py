from app.models.library_item import LibraryItem
from app.models.enums import ItemType


class Book(LibraryItem):
    def __init__(self, title: str, author: str, publication_year: int, isbn: int):
        super().__init__(title, author, ItemType.BOOK)
        self.publication_year = publication_year
        self.isbn = isbn  # International Standard Book Number

    def get_publication_year(self) -> int:
        return self.publication_year

    def set_publication_year(self, publication_year: int):
        self.publication_year = publication_year

    def get_isbn(self) -> int:
        return self.isbn

    def set_isbn(self, isbn: int):
        self.isbn = isbn

    def display_info(self):
        super().display_info()
        print(f"Publication Year: {self.publication_year}")
        print(f"ISBN: {self.isbn}")
