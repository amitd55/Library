import unittest
from unittest.mock import Mock

from classes.SearchManager import SearchManager


class MockBook:
    """Mock book class for testing."""
    def __init__(self, title, author, genre, year, copies_available, popularity_count, is_loaned=False):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.copies_available = copies_available
        self.popularity_count = popularity_count
        self.is_loaned = is_loaned

class TestSearch(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        # Create mock books
        self.books = [
            MockBook("Book A", "Author A", "Fiction", 2020, 5, 100),
            MockBook("Book B", "Author B", "Science", 2019, 0, 50, is_loaned=True),
            MockBook("Book C", "Author C", "Fiction", 2021, 3, 75),
            MockBook("Book D", "Author D", "History", 2018, 0, 30, is_loaned=True),
        ]

        # Create mock book manager
        self.book_manager = Mock()
        self.book_manager.books = self.books

        # Mock logger
        self.logger = Mock()

        # Create SearchManager
        self.search_manager = SearchManager(self.book_manager, self.logger)

    def test_title_search(self):
        """Test title-based search."""
        results = self.search_manager.perform_search("Book A", "title")
        titles = [book.title for book in results]
        self.assertEqual(titles, ["Book A"])

    def test_author_search(self):
        """Test author-based search."""
        results = self.search_manager.perform_search("Author B", "author")
        authors = [book.author for book in results]
        self.assertEqual(authors, ["Author B"])

    def test_genre_search(self):
        """Test genre-based search."""
        results = self.search_manager.perform_search("Fiction", "genre")
        titles = [book.title for book in results]
        self.assertEqual(set(titles), {"Book A", "Book C"})

    def test_year_search(self):
        """Test year-based search."""
        results = self.search_manager.perform_search(2020, "year")
        titles = [book.title for book in results]
        self.assertEqual(titles, ["Book A"])

    def test_copies_available_search(self):
        """Test copies available-based search."""
        results = self.search_manager.perform_search(3, "copies_available")
        titles = [book.title for book in results]
        self.assertEqual(titles, ["Book C"])

    def test_invalid_search_type(self):
        """Test handling of an invalid search type."""
        with self.assertRaises(ValueError):
            self.search_manager.perform_search("Book A", "invalid")

    def test_empty_results(self):
        """Test search returning no results."""
        results = self.search_manager.perform_search("Nonexistent", "title")
        self.assertEqual(len(results), 0)

    def test_display_books_filter(self):
        """Test filtering with display_books."""
        results = self.search_manager.display_books(filter_type="available")
        titles = [book.title for book in results]
        self.assertEqual(titles, ["Book A", "Book C"])

    def test_invalid_filter_type(self):
        """Test handling of an invalid filter type."""
        with self.assertRaises(ValueError):
            self.search_manager.display_books(filter_type="invalid")

if __name__ == "__main__":
    unittest.main()
