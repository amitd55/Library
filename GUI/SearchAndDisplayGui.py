import tkinter as tk
from tkinter import ttk, messagebox
from classes.SearchManager import SearchManager
from classes.BookManager import BookManager
from classes.Logger import Logger

class DisplayBooksGui:
    def __init__(self, search_manager, return_callback):
        self.search_manager = search_manager
        self.return_callback = return_callback
        self.root = tk.Toplevel()
        self.root.title("Book Display Manager")

        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Filter Books:").grid(row=0, column=0, sticky=tk.W)
        self.filter_type = ttk.Combobox(frame, values=["all", "popular", "available", "loaned"])
        self.filter_type.grid(row=0, column=1)
        self.filter_type.set("all")

        ttk.Button(frame, text="Apply Filter", command=self.display_books).grid(row=0, column=2)
        ttk.Button(frame, text="Back", command=self.close).grid(row=0, column=3)

        self.tree = ttk.Treeview(frame, columns=("Title", "Author", "Genre", "Year", "Copies"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Copies", text="Copies Available")
        self.tree.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))

    def display_books(self):
        selected_filter = self.filter_type.get()
        try:
            book_iterator = self.search_manager.display_books(selected_filter)
            self.populate_tree(book_iterator)
        except ValueError as e:
            self.show_error(str(e))

    def populate_tree(self, book_iterator):

        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add books to the tree
        for book in book_iterator:
            self.tree.insert("", tk.END, values=(
                book.title,
                book.author,
                book.genre,
                book.year,
                book.copies_available
            ))

    def show_error(self, message):

        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        ttk.Label(error_window, text=message, padding="10").grid(row=0, column=0)
        ttk.Button(error_window, text="Close", command=error_window.destroy).grid(row=1, column=0)

    def close(self):
        self.root.destroy()
        if self.return_callback:
            self.return_callback()


class SearchBooksGui:
    def __init__(self, root, search_manager, return_callback=None):
        self.root = root
        self.search_manager = search_manager
        self.return_callback = return_callback
        self.root.title("Search Manager")
        self.root.geometry("600x600")  # Set a convenient size for the search window

        # Search frame
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.BOTH, expand=True)

        # Add search input fields and buttons
        self.search_label = tk.Label(self.search_frame, text="Enter query:", font=("Arial", 12))
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 12), width=40)
        self.search_entry.pack(pady=5)

        self.search_type_label = tk.Label(self.search_frame, text="Search type:", font=("Arial", 12))
        self.search_type_label.pack(pady=10)

        self.search_type_combobox = ttk.Combobox(
            self.search_frame, values=["title", "author", "genre", "year", "copies_available"], font=("Arial", 12)
        )
        self.search_type_combobox.pack(pady=5)

        self.search_submit_button = tk.Button(
            self.search_frame, text="Search", font=("Arial", 12, "bold"), bg="lightblue", command=self.perform_search
        )
        self.search_submit_button.pack(pady=10)

        self.results_tree = ttk.Treeview(self.search_frame, columns=("Title", "Author", "Year", "Genre"), show="headings")
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for col in ("Title", "Author", "Year", "Genre"):
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add Return button
        self.return_button = tk.Button(
            self.root, text="Return", font=("Arial", 12, "bold"), bg="lightgreen", command=self.close
        )
        self.return_button.pack(pady=10, side=tk.BOTTOM)

    def perform_search(self):
        query = self.search_entry.get()
        search_type = self.search_type_combobox.get()

        if not query or not search_type:
            error_label = tk.Label(
                self.search_frame, text="Please fill in all fields.", fg="red", font=("Arial", 10, "bold")
            )
            error_label.pack(pady=5)
            self.root.after(3000, error_label.destroy)
            return

        try:
            results_iterator = self.search_manager.perform_search(query, search_type)
            results = list(results_iterator)

            # Clear previous results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)

            if results:
                for book in results:
                    self.results_tree.insert("", "end", values=(book.title, book.author, book.year, book.genre))
            else:
                error_label = tk.Label(
                    self.search_frame, text="No books found.", fg="red", font=("Arial", 10, "bold")
                )
                error_label.pack(pady=5)
                self.root.after(3000, error_label.destroy)
        except ValueError as e:
            error_label = tk.Label(
                self.search_frame, text=f"Error: {str(e)}", fg="red", font=("Arial", 10, "bold")
            )
            error_label.pack(pady=5)
            self.root.after(3000, error_label.destroy)

    def close(self):
        self.root.destroy()
        if self.return_callback:
            self.return_callback()





