import unittest

from classes.BookIterator import BookIterator


class MockBook:
    """Mock book class for testing."""
    def __init__(self, title):
        self.title = title

class TestBookIterator(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.books = [MockBook(f"Book {i}") for i in range(5)]  # Create 5 mock books
        self.empty_books = []
        self.iterator = BookIterator(self.books)
        self.empty_iterator = BookIterator(self.empty_books)

    def test_iteration(self):
        """Test iteration through the BookIterator."""
        titles = [book.title for book in self.iterator]
        expected_titles = [book.title for book in self.books]
        self.assertEqual(titles, expected_titles)

    def test_length(self):
        """Test len()"""
        self.assertEqual(len(self.iterator), len(self.books))
        self.assertEqual(len(self.empty_iterator), 0)

    def test_subscriptable(self):
        """Test subscripting """
        self.assertEqual(self.iterator[0].title, "Book 0")
        self.assertEqual(self.iterator[4].title, "Book 4")
        with self.assertRaises(IndexError):
            _ = self.iterator[5]  # Out-of-range access

    def test_empty_iterator(self):
        """Test behavior of an empty iterator."""
        self.assertEqual(len(self.empty_iterator), 0)
        with self.assertRaises(StopIteration):
            next(iter(self.empty_iterator))

if __name__ == "__main__":
    unittest.main()
