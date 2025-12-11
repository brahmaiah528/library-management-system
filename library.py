import streamlit as st

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


# --- Polymorphic child classes ---
class Fiction(Book):
    def show_details(self):
        return f"[Fiction] {self.title} by {self.author} | Copies: {self.copies}"


class Science(Book):
    def show_details(self):
        return f"[Science] {self.title} by {self.author} | Copies: {self.copies}"


class History(Book):
    def show_details(self):
        return f"[History] {self.title} by {self.author} | Copies: {self.copies}"


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
            return f"Book '{book.title}' issued successfully!"
        else:
            return "No copies left!"

    def return_book(self, book):
        if book.title in self.borrowed_books:
            book.copies += 1
            self.borrowed_books.remove(book.title)
            return f"Book '{book.title}' returned."
        else:
            return "You didn't take this book!"

    def show_my_books(self):
        return self.borrowed_books


# -----------------------
# LIBRARY SYSTEM
# -----------------------
class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.books = [
            Fiction("Harry Potter", "J.K. Rowling", 4),
            Science("Physics Fundamentals", "Halliday", 3),
            History("World War II", "Stephen Ambrose", 2)
        ]

    def register_user(self, phone):
        if phone in self.users:
            return "User already exists!"
        else:
            self.users[phone] = User(phone)
            return "Registration successful!"

    def login(self, phone):
        if phone not in self.users:
            return None
        return self.users[phone]

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None


# ---------------------------------------------
# STREAMLIT FRONTEND
# ---------------------------------------------

if "system" not in st.session_state:
    st.session_state.system = LibrarySystem()
if "current_user" not in st.session_state:
    st.session_state.current_user = None

st.title("📚 Library Management System (Polymorphism)")

system = st.session_state.system

# ---------- LOGIN / REGISTER PAGE ----------
if st.session_state.current_user is None:

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        phone = st.text_input("Enter Phone Number")
        if st.button("Login"):
            user = system.login(phone)
            if user:
                st.session_state.current_user = user
                st.success("Login Successful!")
            else:
                st.error("User not found. Please register.")

    with tab2:
        phone_reg = st.text_input("Enter Phone to Register")
        if st.button("Register"):
            msg = system.register_user(phone_reg)
            st.info(msg)

# ---------- USER DASHBOARD ----------
else:
    user = st.session_state.current_user
    st.subheader(f"Welcome, {user.phone}")

    # View All Books
    st.write("### 📘 Available Books")
    for b in system.books:
        st.write(b.show_details())

    st.write("---")

    # Take book
    st.write("### 📥 Borrow a Book")
    book_name = st.text_input("Enter book name to borrow")
    if st.button("Borrow"):
        book = system.find_book(book_name)
        if book:
            st.success(user.take_book(book))
        else:
            st.error("Book not found!")

    # Return book
    st.write("### 📤 Return a Book")
    return_book_name = st.text_input("Enter book name to return")
    if st.button("Return"):
        book = system.find_book(return_book_name)
        if book:
            st.info(user.return_book(book))
        else:
            st.error("Book not found!")

    # User borrowed books
    st.write("### 📚 My Borrowed Books")
    borrowed = user.show_my_books()
    if borrowed:
        for x in borrowed:
            st.write("•", x)
    else:
        st.write("No books taken yet.")

    if st.button("Logout"):
        st.session_state.current_user = None
        st.success("Logged out!")
