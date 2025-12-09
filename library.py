# ---------------------------------------------
# LIBRARY MANAGEMENT SYSTEM USING POLYMORPHISM
# ---------------------------------------------

class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

    def show_details(self):
        raise NotImplementedError("Subclasses must override this method")


# --- Polymorphism: Each book type overrides show_details() ---
class Fiction(Book):
    def show_details(self):
        print(f"[Fiction] {self.title} by {self.author} | Copies: {self.copies}")


class Science(Book):
    def show_details(self):
        print(f"[Science] {self.title} by {self.author} | Copies: {self.copies}")


class History(Book):
    def show_details(self):
        print(f"[History] {self.title} by {self.author} | Copies: {self.copies}")


# -----------------------
# USER CLASS
# -----------------------
class User:
    def __init__(self, phone):
        self.phone = phone
        self.borrowed_books = []

    def take_book(self, book):
        if book.copies > 0:
            book.copies -= 1
            self.borrowed_books.append(book.title)
            print(f"Book '{book.title}' issued successfully!")
        else:
            print("No copies left!")

    def return_book(self, book):
        if book.title in self.borrowed_books:
            book.copies += 1
            self.borrowed_books.remove(book.title)
            print(f"Book '{book.title}' returned.")
        else:
            print("You didn't take this book!")

    def show_my_books(self):
        print("\nBooks taken by user:")
        for b in self.borrowed_books:
            print(" -", b)
        if not self.borrowed_books:
            print("No books taken yet.")


# -----------------------
# MAIN LIBRARY SYSTEM
# -----------------------
class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.books = [
            Fiction("Harry Potter", "J.K. Rowling", 4),
            Science("Physics Fundamentals", "Halliday", 3),
            History("World War II", "Stephen Ambrose", 2)
        ]

    def register_user(self):
        phone = input("Enter phone number to register: ")
        if phone in self.users:
            print("User already exists!")
        else:
            self.users[phone] = User(phone)
            print("Registration successful!")

    def login(self):
        phone = input("Enter phone number to login: ")
        if phone not in self.users:
            print("User not found. Please register first.")
            return None
        print("Login successful!")
        return self.users[phone]

    def show_all_books(self):
        print("\n--- Available Books ---")
        for book in self.books:
            book.show_details()

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None


# -----------------------
# RUN SYSTEM
# -----------------------
lib = LibrarySystem()

while True:
    print("\n--- LIBRARY MENU ---")
    print("1. Register New User")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        lib.register_user()

    elif choice == "2":
        user = lib.login()
        if user:
            while True:
                print("\n--- USER DASHBOARD ---")
                print("1. View all books")
                print("2. Take a book")
                print("3. Return a book")
                print("4. My borrowed books")
                print("5. Logout")

                c = input("Enter choice: ")

                if c == "1":
                    lib.show_all_books()

                elif c == "2":
                    title = input("Enter book title to borrow: ")
                    book = lib.find_book(title)
                    if book:
                        user.take_book(book)
                    else:
                        print("Book not found!")

                elif c == "3":
                    title = input("Enter book title to return: ")
                    book = lib.find_book(title)
                    if book:
                        user.return_book(book)
                    else:
                        print("Book not found!")

                elif c == "4":
                    user.show_my_books()

                elif c == "5":
                    print("Logged out.")
                    break

                else:
                    print("Invalid choice!")

    elif choice == "3":
        print("Thank you for using the Library System!")
        break

    else:
        print("Invalid choice, try again.")
