class LibraryError(Exception):
    """Base exception for all library domain errors"""
    pass

class BookNotInLibraryError(LibraryError):
    """"Raised when the book does not exist in the library"""
    pass

class UserNotRegisteredError(LibraryError):
    """Raised when the user does not exist or is not registered in the library"""
    pass

class BookAlreadyLoanedError(LibraryError):
    """Raised the Book has already been loaned"""

class BookNotBorrowedByUserError(LibraryError):
    """Raised when a user tries to return a book they did not borrow"""
    pass

class ReturnBookFailedError(LibraryError):
    """Raised when the system is unable to return the book"""
    pass

class LoanNotFoundError(LibraryError):
    """Raised when a loan is not created/found in the library"""
    pass

