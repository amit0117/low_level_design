from app.models.book import Book
from app.models.magazine import Magazine
from app.models.library_item import LibraryItem
from abc import ABC, abstractmethod


class LibraryItemFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_item(title: str, author: str, publication_year: int, isbn: int) -> LibraryItem:
        raise NotImplementedError("Subclasses must implement this method")


class BookFactory(LibraryItemFactory):
    @staticmethod
    def create_item(title: str, author: str, publication_year: int, isbn: int) -> Book:
        return Book(title, author, publication_year, isbn)


class MagazineFactory(LibraryItemFactory):
    @staticmethod
    def create_item(title: str, author: str, publication_year: int, issn: int) -> Magazine:
        return Magazine(title, author, publication_year, issn)


# For now keep only book and magazine
