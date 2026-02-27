from dataclasses import dataclass, field

@dataclass
class Book:
    title: str
    author: str
    isbn: int
    available: bool = field(default=True, init=False)

    def lend(self) -> bool:
        if not self.available:
            return False
        self.available = False
        return True

    def return_book(self) -> bool:
        if self.available:
            return False
        self.available = True
        return True

    def __str__(self) -> str:
        return f"{self.title}. Author: {self.author}, ISBN: {self.isbn}. Available: {self.available}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        return hash(self.isbn)