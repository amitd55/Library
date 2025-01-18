class BookIterator:
    def __init__(self, books):
        if books is None:
            books = []
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration

    def __len__(self):
        return len(self.books)

    def __getitem__(self, index):
        return self.books[index]
