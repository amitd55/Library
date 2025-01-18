from classes.BookFilter import AllBooksFilter, PopularBooksFilter, AvailableBooksFilter, LoanedBooksFilter
from classes.BookIterator import BookIterator
from classes.SearchStrategic import (
    TitleStrategic,
    AuthorStrategic,
    GenreStrategic,
    YearStrategic,
    CopiesAvailableStrategic,
)
from classes.Logger import Logger

class SearchManager:
    def __init__(self, book_manager, logger):
        self.book_manager = book_manager
        self.logger = logger
        self.filters = {
            "all": AllBooksFilter(),
            "popular": PopularBooksFilter(),
            "available": AvailableBooksFilter(),
            "loaned": LoanedBooksFilter(),
        }

    @Logger().log_action
    def perform_search(self, query, search_type):
        """Perform a search using a specified strategy and return an iterator for results."""
        strategy_map = {
            "title": TitleStrategic(self.logger),
            "author": AuthorStrategic(self.logger),
            "genre": GenreStrategic(self.logger),
            "year": YearStrategic(self.logger),
            "copies_available": CopiesAvailableStrategic(self.logger),
        }

        # Select the search strategy
        search_strategy = strategy_map.get(search_type)
        if not search_strategy:
            raise ValueError(f"Invalid search type: {search_type}")

        books = self.book_manager.books
        results = search_strategy.search(books, query)

        # Always return a BookIterator (even if the results list is empty)
        return BookIterator(results)

    @Logger().log_action
    def display_books(self, filter_type="all"):
        """Return an iterator for books based on a filter."""
        filter_strategy = self.filters.get(filter_type)
        if not filter_strategy:
            raise ValueError("Invalid filter type. Use 'all', 'popular', 'available', or 'loaned'.")

        filtered_books = filter_strategy.filter(self.book_manager.books)
        return BookIterator(filtered_books)
