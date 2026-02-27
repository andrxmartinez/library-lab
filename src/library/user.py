from dataclasses import dataclass, field
from typing import List
from .book import Book

@dataclass
class User:
    name: str 
    user_id: int 
    borrowed_books: list[Book] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Welcome, {self.name}, {self.user_id}"

    def add_book(self, book: Book) -> None:
        self.borrowed_books.append(book)

    def remove_book(self, book) -> None:
        self.borrowed_books.remove(book)