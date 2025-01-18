import unittest
from unittest.mock import MagicMock
from classes.BookManager import BookManager
from classes.SearchManager import SearchManager
from classes.Book import Book


class TestSearchManager(unittest.TestCase):
    def setUp(self):
        self.mock_book_manager = MagicMock(spec=BookManager)
        self.mock_books = [
            Book(title="Book1", author="Author1", is_loaned=False, copies=3, genre="Fiction", year=2020),
            Book(title="Book2", author="Author2", is_loaned=True, copies=0, genre="Science", year=2019),
            Book(title="Book3", author="Author3", is_loaned=False, copies=1, genre="Fiction", year=2018)
        ]
        self.mock_book_manager.books = self.mock_books
        self.search_manager = SearchManager(self.mock_book_manager, MagicMock())

    def test_display_all_books(self):
        books = list(self.search_manager.display_books("all"))
        self.assertEqual(len(books), len(self.mock_books))
        self.assertEqual(books[0].title, "Book1")


    def test_display_available_books(self):
        books = list(self.search_manager.display_books("available"))
        self.assertEqual(len(books), 2)  # Book1 and Book3 have copies available
        titles = [book.title for book in books]
        self.assertIn("Book1", titles)
        self.assertIn("Book3", titles)

    def test_display_loaned_books(self):
        books = list(self.search_manager.display_books("loaned"))
        self.assertEqual(len(books), 1)  # Only Book2 is loaned
        self.assertEqual(books[0].title, "Book2")

    def test_invalid_filter_type(self):
        with self.assertRaises(ValueError):
            list(self.search_manager.display_books("invalid"))


if __name__ == "__main__":
    unittest.main()
