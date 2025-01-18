from classes.Observer import Observer
from classes.WaitingListManager import WaitingListManager

class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.loaned_count = self.copies if self.is_loaned else 0
        self.copies_available = 0 if is_loaned else copies
        self.popularity_count= self.loaned_count
        self._waiting_list_manager = None

    @property
    def waiting_list_manager(self):
        """Lazy initialization for the waiting list manager."""
        if self._waiting_list_manager is None:
            self._waiting_list_manager = WaitingListManager()
        return self._waiting_list_manager



    def is_available(self):
        """Check if the book is available for borrowing."""
        return self.copies_available > 0



    def update_details(self, **kwargs):
        """Dynamically update book details."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)



    def to_dict(self):
        """Convert the book object to a dictionary for DataFrame compatibility."""
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.genre,
            "year": self.year,
            "loaned_count": self.loaned_count,
            "waiting_list": self.waiting_list_manager.waiting_list,
            "copies_available": self.copies_available,
            "popularity_count":self.popularity_count
        }

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "
                f"Genre: {self.genre}, Copies: {self.copies}, Loaned: {self.is_loaned}, "
                f"Waiting List: {self.waiting_list_manager.waiting_list}")


