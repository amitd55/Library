from abc import ABC, abstractmethod

class BookFilter(ABC):
    @abstractmethod
    def filter(self, books):
        pass

class AllBooksFilter(BookFilter):
    def filter(self, books):
        return books

class PopularBooksFilter(BookFilter):
    def filter(self, books):
        sorted_books = sorted(books, key=lambda book: book.popularity_count, reverse=True)
        return sorted_books[:10]

class AvailableBooksFilter(BookFilter):
    def filter(self, books):
        return [book for book in books if book.copies_available > 0]

class LoanedBooksFilter(BookFilter):
    def filter(self, books):
        return [book for book in books if book.is_loaned]

class RecentBooksFilter(BookFilter):
    def __init__(self, year):
        self.year = year

    def filter(self, books):
        return [book for book in books if book.year >= self.year]
