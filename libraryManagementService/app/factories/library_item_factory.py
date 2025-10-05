from app.models.book import Book
from app.models.magazine import Magazine
from abc import ABC, abstractmethod


class LibraryItemFactory(ABC):
    @abstractmethod
    def create_item(self):
        raise NotImplementedError("Subclasses must implement this method")


class BookFactory(LibraryItemFactory):
    def __init__(self, title: str, author: str, publication_year: int, isbn: int):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn

    def create_item(self):
        return Book(self.title, self.author, self.publication_year, self.isbn)


class MagazineFactory(LibraryItemFactory):
    def __init__(self, title: str, author: str, publication_year: int, issn: int):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.issn = issn

    def create_item(self):
        return Magazine(self.title, self.author, self.publication_year, self.issn)


# For now keep only book and magazine
