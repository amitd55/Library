from classes.FileHandler import FileHandler
from classes.Logger import Logger
from classes.Book import Book
import pandas as pd


class BookManager:
    def __init__(self):
        self.file_handler = FileHandler()
        self.books = self.load_books()

    def load_books(self):
        try:
            books_data = self.file_handler.load_csv("books.csv")
            if books_data.empty:
                print("books.csv exists but contains no data. Books list remains empty.")
                return []

            return [
                Book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=str(row["is_loaned"]).strip().lower() in ["yes", "true"],
                    copies=int(row["copies"]),
                    genre=row["genre"],
                    year=int(row["year"])
                ) for _, row in books_data.iterrows()
            ]
        except FileNotFoundError:
            print("books.csv not found. Initializing a new file on save.")
            return []
        except Exception as e:
            print(f"Unexpected error loading books: {e}")
            return []

    def book_exists(self, title):
      return any(book.title == title for book in self.books)

    def save_books(self):
        try:
            if not self.books:
                print("No books available to save. Skipping save operation.")
                return
            all_books_df = pd.DataFrame([book.to_dict() for book in self.books])
            loaned_books_df = all_books_df[all_books_df["copies_available"] == 0]
            available_books_df = all_books_df[all_books_df["copies_available"] > 0]
            self.file_handler.save_csv("books.csv", all_books_df)
            self.file_handler.save_csv("loaned_books.csv", loaned_books_df)
            self.file_handler.save_csv("available_books.csv", available_books_df)

        except Exception as e:
            print(f"Error saving books: {e}")

    @Logger().log_action
    def add_book(self, title, author, genre, year, copies):
        """Add a new book or update an existing book."""
        try:
            book = next((b for b in self.books if b.title == title and b.author == author), None)
            if book:
                book.copies += copies
                book.copies_available += copies
                book.is_loaned = book.copies_available == 0
            else:
                new_book = Book(title, author, False, copies, genre, year)
                self.books.append(new_book)

            self.save_books()
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False

    @Logger().log_action
    def remove_book(self, title):
        """Remove a book by title."""
        try:
            existing_book_count = len(self.books)
            self.books = [book for book in self.books if book.title != title]

            if len(self.books) == existing_book_count:
                # No book was removed
                print(f"No book with title '{title}' found.")
                return False

            self.save_books()
            return True
        except Exception as e:
            print(f"Error removing book: {e}")
            return False
