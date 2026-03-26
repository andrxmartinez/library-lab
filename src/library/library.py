from .book import Book
from .user import User
from .loan import Loan
from .exceptions import BookAlreadyRegistered, UserAlreadyRegistered, BookNotInLibraryError, BookNotBorrowedByUserError, UserNotRegisteredError, LoanNotFoundError, BookAlreadyLoanedError, ReturnBookFailedError
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Library:
    name: str
    books: list[Book]  = field(default_factory=list)
    users: list[User] = field(default_factory=list)
    loans: list[Loan] = field(default_factory=list)

    def register_book(self, book:Book) -> bool:
        if book not in self.books:
            self.books.append(book)
            return True
        else:
            raise BookAlreadyRegistered()

    def register_user(self, user:User) -> bool:
        if user not in self.users:
            self.users.append(user)
            return True
        else:
            raise UserAlreadyRegistered()

    def show_available_books(self) -> list[Book]:
        return [book for book in self.books if book.available]

    def show_users(self) -> list[User]:
        return [user for user in self.users]

    def lend_book(self, book:Book, user:User) -> Loan:
        # Initial validations
        if book not in self.books:
            raise BookNotInLibraryError()
        if user not in self.users:
            raise UserNotRegisteredError()
        if not book.lend():
            raise BookAlreadyLoanedError()

        # The library MUST manage the loan internally
        loan = Loan(book, user)

        # Register the loan
        loan.register_loan()

        # Add the loan to the loans list
        self.loans.append(loan)

        # Update the user
        user.add_book(book)

        # Return the active loan
        return loan

    def return_book(self, book: Book, user: User) -> Loan:
        # Initial Validations
        if book not in self.books:
            raise BookNotInLibraryError()
        if user not in self.users:
            raise UserNotRegisteredError()
        if book not in user.borrowed_books:
            raise BookNotBorrowedByUserError()

        # Search for loan
        found_loan = None
        for loan in self.loans:
            if loan.book == book and loan.user == user and loan.is_active():
                found_loan = loan
                break

        # Validate that the loan exists
        if found_loan is None:
            raise LoanNotFoundError()
    
        if not book.return_book():
            raise ReturnBookFailedError()
        
        #Register return
        found_loan.register_return()

        user.remove_book(book)

        return found_loan