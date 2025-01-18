import unittest
from unittest.mock import MagicMock, patch
from classes.BorrowingManager import BorrowingManager
from classes.BookManager import BookManager
from classes.WaitingListManager import WaitingListManager

class TestBorrowingManagerWithWaitingListAndPopularity(unittest.TestCase):

    def setUp(self):
        self.mock_book_manager = MagicMock(spec=BookManager)
        self.mock_waiting_list_manager = MagicMock(spec=WaitingListManager)
        self.mock_book = MagicMock()
        self.mock_book.title = "Test Book"
        self.mock_book.copies_available = 0
        self.mock_book.popularity_count = 0
        self.mock_book.loaned_count = 0
        self.mock_book.waiting_list_manager = self.mock_waiting_list_manager

        self.mock_book_manager.books = [self.mock_book]

        self.borrowing_manager = BorrowingManager()
        self.borrowing_manager.book_manager = self.mock_book_manager

    def test_borrow_book_with_waiting_list_and_popularity(self):
        """Test borrowing a book when no copies are available, updating the waiting list and popularity."""
        self.mock_book.copies_available = 0  #  no available copies

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.borrow_book("Test Book", "user1")

        self.assertTrue(result, "Expected the borrow to succeed by adding the user to the waiting list.")
        self.mock_waiting_list_manager.add_to_waiting_list.assert_called_once_with("user1")
        mock_save_books.assert_called_once()
        self.assertEqual(self.mock_book.popularity_count, 0, "Popularity should not increase when the book is unavailable.")

    def test_borrow_book_available_updates_popularity(self):
        """Test borrowing a book when copies are available updates popularity and loan count."""
        self.mock_book.copies_available = 1  #  1 available copy

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.borrow_book("Test Book", "user2")

        self.assertTrue(result, "Expected the borrow to succeed when copies are available.")
        self.assertEqual(self.mock_book.copies_available, 0, "Copies available should decrease by 1.")
        self.assertEqual(self.mock_book.popularity_count, 1, "Popularity count should increase by 1.")
        self.assertEqual(self.mock_book.loaned_count, 1, "Loaned count should increase by 1.")
        mock_save_books.assert_called_once()

    def test_return_book_with_waiting_list_and_popularity(self):
        """Test returning a book and notifying the next user in the waiting list, updating popularity."""
        self.mock_waiting_list_manager.remove_from_waiting_list.return_value = "user3"
        self.mock_book.copies_available = 0  #  no copies available

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.return_book("Test Book")

        self.assertTrue(result, "Expected the return to succeed and notify the next user in the waiting list.")
        self.mock_waiting_list_manager.remove_from_waiting_list.assert_called_once()
        mock_save_books.assert_called_once()
        self.assertEqual(self.mock_book.copies_available, 1, "Copies available should increase by 1.")
        self.assertEqual(self.mock_book.popularity_count, 0, "Returning a book should not affect popularity count.")

    def test_waiting_list_and_popularity_are_unchanged_when_not_returned(self):
        """Test that waiting list and popularity are unchanged if no book is returned."""
        self.mock_waiting_list_manager.remove_from_waiting_list.return_value = None  # No one in waiting list
        self.mock_book.copies_available = 0

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.return_book("Test Book")

        self.assertTrue(result, "Expected the return to succeed even if the waiting list is empty.")
        self.mock_waiting_list_manager.remove_from_waiting_list.assert_called_once()
        mock_save_books.assert_called_once()
        self.assertEqual(self.mock_book.copies_available, 1, "Copies available should increase by 1.")
        self.assertEqual(self.mock_book.popularity_count, 0, "Popularity count should remain unchanged.")

if __name__ == "__main__":
    unittest.main()
