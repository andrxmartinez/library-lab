import pytest
from library import Library, Book, User, Loan
from library.exceptions import BookAlreadyRegistered, UserAlreadyRegistered, BookNotInLibraryError, BookNotBorrowedByUserError, UserNotRegisteredError, LoanNotFoundError, BookAlreadyLoanedError, ReturnBookFailedError

@pytest.fixture
def library():
    return Library("Lab Library")

@pytest.fixture
def users():
    u1 = User("Steve Test", 1)
    u2 = User("Michaela Test", 2)
    u3 = User("Sophie Test", 3)
    return [u1, u2, u3]

@pytest.fixture
def books():
    b1 = Book("The Alchemist", "Paulo Coehlo", 111)
    b2 = Book("Change Anything", "Grenny Patterson", 112)
    b3 = Book("Harry Potter", "JK Rowling", 113)
    return [b1, b2, b3] 

@pytest.fixture
def book():
    return Book("The Alchemist", "Paulo Coehlo", 111)

@pytest.fixture
def user():
    return User("Steve Test", 1)

#Happy Path 

def test_register_book_success(library, book):
    result = library.register_book(book)
    assert result is True
    assert book in library.books

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

def test_show_available_books_success(library, books, users):

    #Register books
    for book in books:
        library.register_book(book)

    #Register users
    for user in users:
        library.register_user(user)

    #book and user required for lending
    book_to_lend = books[0]
    user_to_lend = users[0]

    #available books
    expected_books = [books[1], books[2]]

    library.lend_book(book_to_lend, user_to_lend)

    #Function validation
    available_books = library.show_available_books()
    assert book_to_lend not in available_books
    assert len(available_books) == 2    

    for book in expected_books:
        assert book in available_books


def test_show_users_success(library, users):
    #Register Users 
    for user in users: 
        library.register_user(user)

    registered_users = library.show_users()
    assert users == registered_users

#Unhappy Path

def test_book_already_registered(library, book):
    library.register_book(book)
    assert book in library.books
    with pytest.raises(BookAlreadyRegistered):
        library.register_book(book)

    #Validate that the book wasn't added again to the library
    assert len(library.books) == 1

def test_user_already_registered(library, user):
    library.register_user(user)
    assert user in library.users
    with pytest.raises(UserAlreadyRegistered):
        library.register_user(user)

    #Validate the user wasn't added again to the library
    assert len(library.users) == 1

@pytest.mark.parametrize(
    "register_book, register_user, expected_exception",
    [
        (False, True, BookNotInLibraryError),
        (True, False, UserNotRegisteredError),
    ]
)
def test_lend_book_errors(library, book, user, register_book, register_user, expected_exception):
    
    if register_book:
        library.register_book(book)
    
    if register_user:
        library.register_user(user)

    with pytest.raises(expected_exception):
        library.lend_book(book, user)
        
def test_lend_book_already_loaned(library, book, user):
    library.register_book(book)
    library.register_user(user)
    library.lend_book(book, user)
    with pytest.raises(BookAlreadyLoanedError):
        library.lend_book(book, user)

@pytest.mark.parametrize(
        "register_book, register_user, complete_loan, expected_exception",
    [   
        (False, True, False, BookNotInLibraryError),
        (True, False, False, UserNotRegisteredError),
        (True, True, False, BookNotBorrowedByUserError)
    ]
        
)
def test_return_book_errors(library, book, user, register_book, register_user, complete_loan, expected_exception):
      
    if register_book:
        library.register_book(book)

    if register_user:
        library.register_user(user)

    if complete_loan:
        library.register_book(book)
        library.register_user(user)
        library.lend_book(book, user)

    with pytest.raises(expected_exception):
        library.return_book(book, user)       

def test_return_loan_not_found(library, book, user):
    library.register_book(book)
    library.register_user(user)
    loan = library.lend_book(book, user)
  
    #This manually breaks the system to trigger the error (Simulates corrupt state)
    library.loans.remove(loan)

    with pytest.raises(LoanNotFoundError):
        library.return_book(book, user)

#Adds a monkeypatch to force return_book() to return False for testing purposes
def test_return_loan_failed(monkeypatch, library, book, user):
    library.register_book(book)
    library.register_user(user)
    loan = library.lend_book(book, user)

    #fake return
    def fake_return():
        return False
    
    #Replaces real method
    monkeypatch.setattr(book, "return_book", fake_return)

    #Validate exception
    with pytest.raises(ReturnBookFailedError):
        library.return_book(book, user)

    assert loan in library.loans
    assert  loan.is_active()
    assert book in user.borrowed_books
    assert not book.available



