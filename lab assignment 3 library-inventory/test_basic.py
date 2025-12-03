from library_manager.book import Book

def test_book_available():
    b = Book("Test", "Author", "123")
    assert b.is_available()
