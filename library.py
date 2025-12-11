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
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
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

    def change_password(self, new_password):
        self.password = new_password
        return "Password updated successfully!"

# -----------------------
# LIBRARY SYSTEM
# -----------------------
class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.books = [
            Fiction("Harry Potter", "J.K. Rowling", 4),
            Fiction("The Hobbit", "J.R.R. Tolkien", 3),
            Fiction("Pride and Prejudice", "Jane Austen", 3),
            Science("Physics Fundamentals", "Halliday", 3),
            Science("Chemistry Basics", "Zumdahl", 2),
            Science("Biology 101", "Campbell", 2),
            History("World War II", "Stephen Ambrose", 2),
            History("Ancient Civilizations", "Will Durant", 2),
            History("Modern History", "Eric Hobsbawm", 2),
            Fiction("To Kill a Mockingbird", "Harper Lee", 3),
            Fiction("1984", "George Orwell", 2),
            Science("Astronomy Today", "Chaisson", 2),
            Science("Computer Science", "Tanenbaum", 2),
            History("History of India", "Romila Thapar", 2),
            Fiction("The Great Gatsby", "F. Scott Fitzgerald", 2),
            Science("Mathematics for Beginners", "Stewart", 2),
            History("French Revolution", "Schama", 2),
            Fiction("Moby Dick", "Herman Melville", 2),
            Science("Quantum Physics", "Griffiths", 2),
            History("Cold War", "John Lewis Gaddis", 2)
        ]
        # Admin user
        self.users["admin"] = User("admin", "admin123")

    def register_user(self, phone, password):
        if phone in self.users:
            return "User already exists!"
        else:
            self.users[phone] = User(phone, password)
            return "Registration successful!"

    def login(self, phone, password):
        if phone in self.users and self.users[phone].password == password:
            return self.users[phone]
        return None

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def search_books(self, query):
        results = []
        query = query.lower()
        for book in self.books:
            if query in book.title.lower() or query in book.author.lower():
                results.append(book)
        return results

    def add_book(self, title, author, copies, category):
        if category.lower() == "fiction":
            self.books.append(Fiction(title, author, copies))
        elif category.lower() == "science":
            self.books.append(Science(title, author, copies))
        elif category.lower() == "history":
            self.books.append(History(title, author, copies))
        else:
            return "Invalid category!"
        return f"Book '{title}' added successfully!"

    def delete_book(self, title):
        book = self.find_book(title)
        if book:
            self.books.remove(book)
            return f"Book '{title}' deleted successfully!"
        else:
            return "Book not found!"

    def delete_user(self, phone):
        if phone in self.users and phone != "admin":
            del self.users[phone]
            return f"User '{phone}' deleted successfully!"
        elif phone == "admin":
            return "Cannot delete admin!"
        else:
            return "User not found!"

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
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = system.login(phone, password)
            if user:
                st.session_state.current_user = user
                st.success("Login Successful!")
            else:
                st.error("Invalid credentials!")

    with tab2:
        phone_reg = st.text_input("Phone to Register", key="reg_phone")
        password_reg = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            msg = system.register_user(phone_reg, password_reg)
            st.info(msg)

# ---------- USER DASHBOARD ----------
else:
    user = st.session_state.current_user
    st.subheader(f"Welcome, {user.phone}")

    if user.phone == "admin":
        menu = st.selectbox("Select Action", [
            "View/Search Books", "Add Book", "Delete Book",
            "View Users", "Delete User", "Change Password", "Logout"
        ])

        if menu == "View/Search Books":
            st.write("### 📘 All Books")
            query = st.text_input("Search by title or author", key="admin_search")
            results = system.search_books(query) if query else system.books
            if results:
                for b in results:
                    st.write(b.show_details())
            else:
                st.write("No matching books found.")

        elif menu == "Add Book":
            st.write("### ➕ Add New Book")
            new_title = st.text_input("Book Title", key="admin_title")
            new_author = st.text_input("Author", key="admin_author")
            new_copies = st.number_input("Copies", min_value=1, step=1, key="admin_copies")
            new_category = st.selectbox("Category", ["Fiction", "Science", "History"], key="admin_category")
            if st.button("Add Book", key="admin_add"):
                msg = system.add_book(new_title, new_author, new_copies, new_category)
                st.success(msg)

        elif menu == "Delete Book":
            del_book_title = st.text_input("Enter Book Title to Delete", key="del_book")
            if st.button("Delete Book", key="del_book_btn"):
                msg = system.delete_book(del_book_title)
                st.info(msg)

        elif menu == "View Users":
            st.write("### 👥 Registered Users & Borrowed Books")
            for u in system.users.values():
                st.write(f"User: {u.phone}, Borrowed Books: {u.borrowed_books}")

        elif menu == "Delete User":
            del_user_phone = st.text_input("Enter User Phone to Delete", key="del_user")
            if st.button("Delete User", key="del_user_btn"):
                msg = system.delete_user(del_user_phone)
                st.info(msg)

        elif menu == "Change Password":
            new_pass = st.text_input("Enter New Password", type="password", key="admin_new_pass")
            if st.button("Update Password"):
                msg = user.change_password(new_pass)
                st.success(msg)

        elif menu == "Logout":
            st.session_state.current_user = None
            st.success("Logged out!")

    else:
        menu = st.selectbox("Select Action", [
            "View/Search Books", "Borrow Book", "Return Book",
            "My Borrowed Books", "Change Password", "Logout"
        ])

        if menu == "View/Search Books":
            st.write("### 📘 Available Books")
            query = st.text_input("Search by title or author", key="user_search")
            results = system.search_books(query) if query else system.books
            if results:
                for b in results:
                    st.write(b.show_details())
            else:
                st.write("No matching books found.")

        elif menu == "Borrow Book":
            book_name = st.text_input("Enter book name to borrow", key="borrow")
            if st.button("Borrow"):
                book = system.find_book(book_name)
                if book:
                    st.success(user.take_book(book))
                else:
                    st.error("Book not found!")

        elif menu == "Return Book":
            return_book_name = st.text_input("Enter book name to return", key="return")
            if st.button("Return"):
                book = system.find_book(return_book_name)
                if book:
                    st.info(user.return_book(book))
                else:
                    st.error("Book not found!")

        elif menu == "My Borrowed Books":
            borrowed = user.show_my_books()
            st.write("### 📚 My Borrowed Books")
            if borrowed:
                for x in borrowed:
                    st.write("•", x)
            else:
                st.write("No books taken yet.")

        elif menu == "Change Password":
            new_pass = st.text_input("Enter New Password", type="password", key="user_new_pass")
            if st.button("Update Password"):
                msg = user.change_password(new_pass)
                st.success(msg)

        elif menu == "Logout":
            st.session_state.current_user = None
            st.success("Logged out!")
