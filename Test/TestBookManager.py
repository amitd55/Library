import unittest
from unittest.mock import MagicMock
from classes.Book import Book
from classes.BookManager import BookManager
import pandas as pd

class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.mock_file_handler = MagicMock()
        self.book_manager = BookManager()
        self.book_manager.file_handler = self.mock_file_handler

    def test_add_new_book(self):
        #  initial empty data
        self.mock_file_handler.load_csv.return_value = pd.DataFrame()
        self.book_manager.books = []

        # Add a new book
        result = self.book_manager.add_book("New Book", "Author", "Genre", 2023, 3)

        # Verify
        self.assertTrue(result)
        self.assertEqual(len(self.book_manager.books), 1)
        self.assertEqual(self.book_manager.books[0].title, "New Book")
        self.assertEqual(self.book_manager.books[0].copies, 3)

    def test_increase_copies_existing_book(self):
        # Mock data with one book
        existing_book = Book("Existing Book", "Author", False, 2, "Genre", 2021)
        self.book_manager.books = [existing_book]

        # Increase copies of the existing book
        result = self.book_manager.add_book("Existing Book", "Author", "Genre", 2021, 5)

        # Verify
        self.assertTrue(result)
        self.assertEqual(self.book_manager.books[0].copies, 7)

    def test_move_loaned_to_available(self):
        # Mock data with a loaned book
        loaned_book = Book("Loaned Book", "Author", True, 1, "Genre", 2020)
        loaned_book.copies_available = 0
        self.book_manager.books = [loaned_book]

        # Increase copies of the loaned book
        result = self.book_manager.add_book("Loaned Book", "Author", "Genre", 2020, 3)

        # Verify
        self.assertTrue(result)
        self.assertEqual(self.book_manager.books[0].copies, 4)
        self.assertEqual(self.book_manager.books[0].copies_available, 3)
        self.assertFalse(self.book_manager.books[0].is_loaned)

    def test_remove_book(self):
        # Mock data with books
        book1 = Book("Book1", "Author1", False, 2, "Genre1", 2020)
        book2 = Book("Book2", "Author2", False, 1, "Genre2", 2021)
        self.book_manager.books = [book1, book2]

        # Remove a book
        result = self.book_manager.remove_book("Book1")

        # Verify
        self.assertTrue(result)
        self.assertEqual(len(self.book_manager.books), 1)
        self.assertEqual(self.book_manager.books[0].title, "Book2")

    def test_save_books(self):
        book1 = Book("Book1", "Author1", False, 2, "Genre1", 2020)
        self.book_manager.books = [book1]

        # Call save_books
        self.book_manager.save_books()

        # Verify save_csv calls
        self.mock_file_handler.save_csv.assert_any_call("books.csv", unittest.mock.ANY)
        self.mock_file_handler.save_csv.assert_any_call("loaned_books.csv", unittest.mock.ANY)
        self.mock_file_handler.save_csv.assert_any_call("available_books.csv", unittest.mock.ANY)

    def test_load_books_empty(self):
        #  an empty file
        self.mock_file_handler.load_csv.return_value = pd.DataFrame()

        books = self.book_manager.load_books()

        self.assertEqual(len(books), 0)

    def test_load_books_with_data(self):
        #  a file with data
        data = pd.DataFrame({
            "title": ["Book1", "Book2"],
            "author": ["Author1", "Author2"],
            "is_loaned": ["False", "True"],
            "copies": [2, 1],
            "genre": ["Genre1", "Genre2"],
            "year": [2020, 2021]
        })
        self.mock_file_handler.load_csv.return_value = data

        books = self.book_manager.load_books()

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Book1")
        self.assertTrue(books[1].is_loaned)


if __name__ == "__main__":
    unittest.main()
