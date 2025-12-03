import json
import logging
from pathlib import Path
from .book import Book

class LibraryInventory:
    def __init__(self, filepath="data/catalog.json"):
        self.filepath = Path(filepath)
        self.books = []
        self.load_catalog()

    def load_catalog(self):
        try:
            if not self.filepath.exists():
                self.filepath.parent.mkdir(exist_ok=True)
                self.filepath.write_text("[]")
            data = json.loads(self.filepath.read_text())
            self.books = [Book(**b) for b in data]
        except Exception as e:
            logging.error(f"Error loading catalog: {e}")
            self.books = []

    def save_catalog(self):
        try:
            data = [b.to_dict() for b in self.books]
            self.filepath.write_text(json.dumps(data, indent=4))
        except Exception as e:
            logging.error(f"Error saving catalog: {e}")

    def add_book(self, title, author, isbn):
        self.books.append(Book(title, author, isbn))
        logging.info(f"Added new book: {title}")
        self.save_catalog()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def display_all(self):
        return self.books
