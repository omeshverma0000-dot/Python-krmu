import logging

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if self.is_available():
            self.status = "issued"
            logging.info(f"Book issued: {self.title}")
            return True
        logging.error(f"Attempt to issue unavailable book: {self.title}")
        return False

    def return_book(self):
        self.status = "available"
        logging.info(f"Book returned: {self.title}")
