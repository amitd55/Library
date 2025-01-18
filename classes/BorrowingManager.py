from classes.BookManager import BookManager
from classes.Logger import Logger



class BorrowingManager:

    def __init__(self):
        self.book_manager = BookManager()

    @Logger().log_action
    def borrow_book(self, title, username=None):
        """Borrow a book or add the user to the waiting list if unavailable."""
        try:
            book = next((b for b in self.book_manager.books if b.title == title), None)
            if not book:
                print(f"Error: Book '{title}' not found.")
                return False

            # Check if the book is available
            if book.copies_available > 0:
                book.copies_available -= 1
                book.loaned_count += 1
                book.popularity_count += 1

                # Update `is_loaned` status
                if book.copies_available == 0:
                    book.is_loaned = True

                self.book_manager.save_books()
                print(f"Book '{title}' borrowed by {username or 'anonymous'}.")
                return True
            else:
                # Book is unavailable; add the user to the waiting list
                if username:
                    book.waiting_list_manager.add_to_waiting_list(username)
                    print(f"{username} added to the waiting list for '{title}'.")
                    self.book_manager.save_books()
                    return True
                else:
                    print(f"Book '{title}' is unavailable, and no user name provided for the waiting list.")
                    return False
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False

    @Logger().log_action
    def return_book(self, title):
        """Return a book and notify the next user in the waiting list."""
        try:
            book = next((b for b in self.book_manager.books if b.title == title), None)
            if not book:
                print(f"Error: Book '{title}' not found.")
                return False

            # Increment available copies
            book.copies_available += 1
            if book.copies_available > 0:
                book.is_loaned = False  # Mark the book as not loaned

            # Notify the next user in the waiting list
            next_user = book.waiting_list_manager.remove_from_waiting_list()
            if next_user:
                print(f"Notification: The book '{title}' is now available for {next_user}.")
            else:
                print(f"No users in the waiting list for '{title}'.")
            self.book_manager.save_books()
            return True
        except Exception as e:
            print(f"Error returning book: {e}")
            return False
