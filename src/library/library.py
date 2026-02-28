from .book import Book
from .user import User
from .loan import Loan
from .exceptions import BookNotInLibraryError, BookNotBorrowedByUserError, UserNotRegisteredError, LoanNotFoundError, BookAlreadyLoanedError, ReturnBookFailedError
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
            return False

    def register_user(self, user:User) -> bool:
        if user not in self.users:
            self.users.append(user)
            return True
        else:
            return False

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

    def return_book(self, book:Book, user:User) -> Loan:
        # Initial validations
        if book not in self.books:
            raise BookNotInLibraryError()
        if user not in self.users:
            raise UserNotRegisteredError()
        if book not in user.borrowed_books:
            raise BookNotBorrowedByUserError()

        # Attempt to return the book
        if not book.return_book():
            raise ReturnBookFailedError()

        # Search for active loan
        found_loan = None
        for loan in self.loans:
            if loan.book == book and loan.user == user and loan.is_active():
                loan.register_return()
                found_loan = loan
                break

        # Validate that the loan was found
        if found_loan is None:
            raise LoanNotFoundError()

        # Update user
        user.remove_book(book)

        # Return closed loan
        return found_loan