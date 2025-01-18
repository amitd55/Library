import unittest
from unittest.mock import MagicMock, patch
from classes.BorrowingManager import BorrowingManager
from classes.BookManager import BookManager
from classes.WaitingListManager import WaitingListManager

class TestBorrowingManagerWithWaitingList(unittest.TestCase):

    def setUp(self):
        self.mock_book_manager = MagicMock(spec=BookManager)
        self.mock_waiting_list_manager = MagicMock(spec=WaitingListManager)

        self.mock_book = MagicMock()
        self.mock_book.title = "Test Book"
        self.mock_book.copies_available = 0
        self.mock_book.waiting_list_manager = self.mock_waiting_list_manager
        self.mock_book_manager.books = [self.mock_book]
        self.borrowing_manager = BorrowingManager()
        self.borrowing_manager.book_manager = self.mock_book_manager

    def test_borrow_book_with_waiting_list(self):
        """Test borrowing a book when no copies are available, with waiting list functionality."""
        self.mock_book.copies_available = 0  #  no available copies

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.borrow_book("Test Book", "user1")

        self.assertTrue(result, "Expected the borrow to succeed by adding the user to the waiting list.")
        self.mock_waiting_list_manager.add_to_waiting_list.assert_called_once_with("user1")
        mock_save_books.assert_called_once()

    def test_return_book_with_waiting_list(self):
        """Test returning a book and notifying the next user in the waiting list."""
        self.mock_waiting_list_manager.remove_from_waiting_list.return_value = "user2"
        self.mock_book.copies_available = 0  #  no copies available

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.return_book("Test Book")

        self.assertTrue(result, "Expected the return to succeed and notify the next user in the waiting list.")
        self.mock_waiting_list_manager.remove_from_waiting_list.assert_called_once()
        mock_save_books.assert_called_once()
        self.assertEqual(self.mock_book.copies_available, 1, "Copies available should increase by 1.")

    def test_borrow_book_not_in_waiting_list(self):
        """Test borrowing a book when user is not in the waiting list."""
        self.mock_book.copies_available = 0

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.borrow_book("Test Book", "user3")

        self.assertTrue(result, "Expected the user to be added to the waiting list.")
        self.mock_waiting_list_manager.add_to_waiting_list.assert_called_once_with("user3")
        mock_save_books.assert_called_once()

    def test_waiting_list_is_empty_on_return(self):
        """Test returning a book when there are no users in the waiting list."""
        self.mock_waiting_list_manager.remove_from_waiting_list.return_value = None  # No one in waiting list
        self.mock_book.copies_available = 0

        with patch.object(self.borrowing_manager.book_manager, 'save_books') as mock_save_books:
            result = self.borrowing_manager.return_book("Test Book")

        self.assertTrue(result, "Expected the return to succeed even if the waiting list is empty.")
        self.mock_waiting_list_manager.remove_from_waiting_list.assert_called_once()
        mock_save_books.assert_called_once()
        self.assertEqual(self.mock_book.copies_available, 1, "Copies available should increase by 1.")

if __name__ == "__main__":
    unittest.main()
