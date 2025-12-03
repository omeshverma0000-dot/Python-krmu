import logging
from library_manager.inventory import LibraryInventory

logging.basicConfig(filename="library.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def menu():
    print("\n--- Library Inventory Manager ---")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")

def main():
    inventory = LibraryInventory()

    while True:
        menu()
        choice = input("Enter choice: ")

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                inventory.add_book(title, author, isbn)
                print("Book added successfully.")

            elif choice == "2":
                isbn = input("Enter ISBN: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_catalog()
                    print("Book issued.")
                else:
                    print("Book not available.")

            elif choice == "3":
                isbn = input("Enter ISBN: ")
                book = inventory.search_by_isbn(isbn)
                if book:
                    book.return_book()
                    inventory.save_catalog()
                    print("Book returned.")
                else:
                    print("Book not found.")

            elif choice == "4":
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                title = input("Enter title search: ")
                results = inventory.search_by_title(title)
                for b in results:
                    print(b)
                if not results:
                    print("No books found.")

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            logging.error(f"Runtime error: {e}")
            print("An error occurred. Check logs.")

if __name__ == "__main__":
    main()
