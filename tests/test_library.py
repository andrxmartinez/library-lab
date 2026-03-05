import pytest
from library import Library, Book, User, Loan
from library.exceptions import BookNotInLibraryError, BookNotBorrowedByUserError, UserNotRegisteredError, LoanNotFoundError, BookAlreadyLoanedError

@pytest.fixture
def library():
    return Library("Lab Library") 

@pytest.fixture
def book():
    return Book("The Alchemist", "Paulo Coehlo", 111)
def b2():
    return Book("Change Anything", "Grenny Patterson", 112)
def b3():
    return Book("Harry Potter", "JK Rowling", 113)


@pytest.fixture
def user():
    return User("Steve Test", 1)
def u2():
    return User("Michaela Test", 2)
def u3():
    return User("Sophie Test", 3)

#Happy Path 

# @pytest.mark.parametrize("book", [b1, b2, b3])
def test_register_book_success(library, book):
    result = library.register_book(book)
    assert result is True
    assert book in library.books

# @pytest.mark.parametrize("user", [u1, u2, u3])
def test_register_user_success(library, user):
    result = library.register_user(user)
    assert result is True
    assert user in library.users

def test_lend_book_success(library, book, user):
    library.register_book(book)
    library.register_user(user)
    loan = library.lend_book(book, user)
    assert loan in library.loans
    assert loan.is_active()

def test_return_book_success(library, book, user):
    library.register_book(book)
    library.register_user(user)
    loan = library.lend_book(book, user)
    library.return_book(book, user)
    assert not loan.is_active()
    assert book.available
    assert book not in user.borrowed_books

#Unhappy Path

def test_lend_book_not_registered(library, book, user):
    library.register_user(user)
    with pytest.raises(BookNotInLibraryError):
        library.lend_book(book, user)

def test_lend_user_not_registered(library, book, user):
    library.register_book(book)
    with pytest.raises(UserNotRegisteredError):
        library.lend_book(book, user)

def test_lend_book_already_loaned(library, book, user):
    library.register_book(book)
    library.register_user(user)
    library.lend_book(book, user)
    with pytest.raises(BookAlreadyLoanedError):
        library.lend_book(book, user)

def test_return_book_not_in_library(library, book, user):
    library.register_user(user)
    with pytest.raises(BookNotInLibraryError):
        library.return_book(book, user)


def test_return_user_not_registered(library, book, user):
    library.register_book(book)
    with pytest.raises(UserNotRegisteredError):
        library.return_book(book, user)

def test_return_book_not_borrowed(library, book, user):
    library.register_book(book)
    library.register_user(user)
    with pytest.raises(BookNotBorrowedByUserError):
        library.return_book(book, user)

def test_return_loan_not_found(library, book, user):
    library.register_book(book)
    library.register_user(user)
    loan = library.lend_book(book, user)
  
    #This manually breaks the system to trigger the error (Simulates corrupt state)
    library.loans.remove(loan)

    with pytest.raises(LoanNotFoundError):
        library.return_book(book, user)



