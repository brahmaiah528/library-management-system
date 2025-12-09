import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re

st.set_page_config(page_title="Library Management System", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_phone = None
    st.session_state.user_name = None

# Sample Database
USERS_DB = {
    "user1@gmail.com": {
        "password": "pass123",
        "name": "Raj Kumar",
        "phone": "9876543210",
        "borrowed_books": ["B001", "B003"]
    },
    "9876543210": {
        "password": "pass123",
        "name": "Priya Sharma",
        "email": "priya@gmail.com",
        "borrowed_books": ["B002"]
    },
    "user2@gmail.com": {
        "password": "pass456",
        "name": "Amit Singh",
        "phone": "9123456789",
        "borrowed_books": []
    }
}

BOOKS_DB = {
    "B001": {
        "title": "Data Structures in C++",
        "author": "Mark Allen Weiss",
        "isbn": "978-0201361369",
        "quantity": 3,
        "available": 1,
        "category": "Computer Science"
    },
    "B002": {
        "title": "Algorithms Unlocked",
        "author": "Thomas H. Cormen",
        "isbn": "978-0262518802",
        "quantity": 5,
        "available": 4,
        "category": "Computer Science"
    },
    "B003": {
        "title": "Introduction to IoT",
        "author": "David Easley",
        "isbn": "978-0262527118",
        "quantity": 2,
        "available": 0,
        "category": "IoT/Embedded"
    },
    "B004": {
        "title": "Python for Data Science",
        "author": "Wes McKinney",
        "isbn": "978-1491957653",
        "quantity": 4,
        "available": 4,
        "category": "Programming"
    },
    "B005": {
        "title": "Graph Theory Handbook",
        "author": "Jonathan Gross",
        "isbn": "978-1439880179",
        "quantity": 2,
        "available": 2,
        "category": "Mathematics"
    },
    "B006": {
        "title": "Discrete Mathematics",
        "author": "Richard Johnsonbaugh",
        "isbn": "978-0134689517",
        "quantity": 3,
        "available": 2,
        "category": "Mathematics"
    }
}

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email)

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    return re.match(r'^[6-9]\d{9}$', phone)

def login_page():
    st.markdown("<h1 style='text-align: center;'>📚 Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Login to Access Your Account</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        login_method = st.radio("Select Login Method:", ["Gmail", "Phone Number"], horizontal=True)
        
        if login_method == "Gmail":
            email = st.text_input("📧 Enter Gmail Address", placeholder="example@gmail.com")
            password = st.text_input("🔐 Enter Password", type="password")
            
            if st.button("Login with Gmail", use_container_width=True):
                if not email:
                    st.error("Please enter email")
                elif not validate_email(email):
                    st.error("Invalid Gmail format (use @gmail.com)")
                elif email not in USERS_DB:
                    st.error("Email not found in system")
                elif USERS_DB[email]["password"] != password:
                    st.error("Invalid password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_name = USERS_DB[email]["name"]
                    st.session_state.user_phone = USERS_DB[email].get("phone", "N/A")
                    st.success(f"Welcome, {st.session_state.user_name}!")
                    st.rerun()
        
        else:  # Phone Number Login
            phone = st.text_input("📱 Enter Phone Number (10 digits)", placeholder="9876543210")
            password = st.text_input("🔐 Enter Password", type="password")
            
            if st.button("Login with Phone", use_container_width=True):
                if not phone:
                    st.error("Please enter phone number")
                elif not validate_phone(phone):
                    st.error("Invalid phone format (10 digits, starting with 6-9)")
                elif phone not in USERS_DB:
                    st.error("Phone number not registered")
                elif USERS_DB[phone]["password"] != password:
                    st.error("Invalid password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.user_name = USERS_DB[phone]["name"]
                    st.session_state.user_email = USERS_DB[phone].get("email", "N/A")
                    st.success(f"Welcome, {st.session_state.user_name}!")
                    st.rerun()
        
        st.markdown("---")
        st.info("Demo Credentials:\n- Email: user1@gmail.com | Pass: pass123\n- Phone: 9876543210 | Pass: pass123")

def dashboard_page():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"<h1>Welcome, {st.session_state.user_name}! 👋</h1>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_phone = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown("---")
    
    # User Info
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📧 Email", st.session_state.user_email if st.session_state.user_email else "N/A")
    with col2:
        st.metric("📱 Phone", st.session_state.user_phone if st.session_state.user_phone else "N/A")
    
    st.markdown("---")
    
    # Get user's borrowed books
    user_key = st.session_state.user_email if st.session_state.user_email else st.session_state.user_phone
    borrowed_book_ids = USERS_DB[user_key].get("borrowed_books", [])
    
    # Tabs for navigation
    tab1, tab2 = st.tabs(["📚 My Borrowed Books", "📖 Available Books in Library"])
    
    with tab1:
        st.subheader("Your Borrowed Books")
        
        if not borrowed_book_ids:
            st.info("You haven't borrowed any books yet.")
        else:
            borrowed_books_data = []
            for book_id in borrowed_book_ids:
                if book_id in BOOKS_DB:
                    book = BOOKS_DB[book_id]
                    borrowed_date = datetime.now() - timedelta(days=15)
                    due_date = borrowed_date + timedelta(days=30)
                    
                    borrowed_books_data.append({
                        "Book ID": book_id,
                        "Title": book["title"],
                        "Author": book["author"],
                        "Category": book["category"],
                        "ISBN": book["isbn"],
                        "Borrowed Date": borrowed_date.strftime("%Y-%m-%d"),
                        "Due Date": due_date.strftime("%Y-%m-%d")
                    })
            
            df_borrowed = pd.DataFrame(borrowed_books_data)
            st.dataframe(df_borrowed, use_container_width=True, hide_index=True)
            
            st.metric("Total Books Borrowed", len(borrowed_book_ids))
    
    with tab2:
        st.subheader("Available Books in Library")
        
        # Count available books
        total_books = len(BOOKS_DB)
        available_books_count = sum(1 for book in BOOKS_DB.values() if book["available"] > 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Total Books", total_books)
        with col2:
            st.metric("✅ Available", available_books_count)
        with col3:
            st.metric("❌ Not Available", total_books - available_books_count)
        
        st.markdown("---")
        
        # Filter by category
        categories = ["All"] + sorted(set(book["category"] for book in BOOKS_DB.values()))
        selected_category = st.selectbox("Filter by Category:", categories)
        
        # Search by title
        search_title = st.text_input("Search by Book Title or Author:")
        
        # Build books table
        books_data = []
        for book_id, book in BOOKS_DB.items():
            # Apply filters
            if selected_category != "All" and book["category"] != selected_category:
                continue
            if search_title and search_title.lower() not in book["title"].lower() and search_title.lower() not in book["author"].lower():
                continue
            
            status = "✅ Available" if book["available"] > 0 else "❌ Not Available"
            
            books_data.append({
                "Book ID": book_id,
                "Title": book["title"],
                "Author": book["author"],
                "Category": book["category"],
                "ISBN": book["isbn"],
                "Total Copies": book["quantity"],
                "Available": book["available"],
                "Status": status
            })
        
        if books_data:
            df_books = pd.DataFrame(books_data)
            st.dataframe(df_books, use_container_width=True, hide_index=True)
        else:
            st.warning("No books match your search criteria.")
        
        st.markdown("---")
        st.info(f"Total matching books: {len(books_data)}")

# Main App Logic
if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()