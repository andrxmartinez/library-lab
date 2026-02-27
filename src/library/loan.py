from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional
from .book import Book
from .user import User

@dataclass
class Loan:
    loan_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    book: Optional[Book] = None
    user: Optional[User] = None
    status: bool = False

    def register_loan(self) -> None:
        self.status = True
        self.loan_date = datetime.now()
        self.return_date = self.loan_date + timedelta(days=15)

    def register_return(self) -> None:
        self.status = False
        self.return_date = datetime.now()

    def is_active(self) -> bool:
        return self.status