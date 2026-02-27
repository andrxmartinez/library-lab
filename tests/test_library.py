from library import Library, Book, User


def test_register_book_success():
    library = Library("Test Library")
    book = Book("1984", "Orwell", "123")

    result = library.register_book(book)

    assert result is True
    assert book in library.books