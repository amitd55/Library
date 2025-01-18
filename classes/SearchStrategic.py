from abc import ABC, abstractmethod
from classes.Logger import Logger
from classes.BookIterator import BookIterator  # Assuming BookIterator is implemented

class SearchStrategic(ABC):
    def __init__(self, logger):
        self.logger = logger

    @Logger().log_action
    def search(self, books, query):
        """Template for search logic."""
        results = self._perform_search(books, query)

        # Return a BookIterator (even for empty results)
        return BookIterator(results)

    @abstractmethod
    def _perform_search(self, books, query):
        pass


class TitleStrategic(SearchStrategic):
    def _perform_search(self, books, query):
        return [book for book in books if query.lower() in book.title.lower()]


class AuthorStrategic(SearchStrategic):
    def _perform_search(self, books, query):
        return [book for book in books if query.lower() in book.author.lower()]


class GenreStrategic(SearchStrategic):
    def _perform_search(self, books, query):
        return [book for book in books if query.lower() in book.genre.lower()]


class YearStrategic(SearchStrategic):
    def _perform_search(self, books, query):
        return [book for book in books if str(query) == str(book.year)]


class CopiesAvailableStrategic(SearchStrategic):
    def _perform_search(self, books, query):
        return [book for book in books if book.copies_available == int(query)]
