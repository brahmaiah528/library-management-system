import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re
import json

st.set_page_config(page_title="Library Management System", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_phone = None
    st.session_state.user_name = None

# Initialize Users Database (Persistent in session)
if "users_db" not in st.session_state:
    st.session_state.users_db = {
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
        },
        "9123456789": {
            "password": "pass456",
            "name": "Amit Singh",
            "email": "user2@gmail.com",
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

def validate_password(password):
    """Validate password (min 6 characters)"""
    return len(password) >= 6

def signup_page():
    st.markdown("<h1 style='text-align: center;'>📚 Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Create Your Account</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        
        # Sign Up Form
        name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Gmail Address", placeholder="example@gmail.com")
        phone = st.text_input("📱 Phone Number (10 digits)", placeholder="9876543210")
        password = st.text_input("🔐 Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("🔐 Confirm Password", type="password")
        
        if st.button("Create Account", use_container_width=True, type="primary"):
            # Validation
            if not name:
                st.error("❌ Please enter your name")
            elif not email:
                st.error("❌ Please enter email")
            elif not validate_email(email):
                st.error("❌ Invalid Gmail format (use @gmail.com)")
            elif email in st.session_state.users_db:
                st.error("❌ Email already registered")
            elif not phone:
                st.error("❌ Please enter phone number")
            elif not validate_phone(phone):
                st.error("❌ Invalid phone format (10 digits, starting with 6-9)")
            elif phone in st.session_state.users_db:
                st.error("❌ Phone number already registered")
            elif not password:
                st.error("❌ Please enter password")
            elif not validate_password(password):
                st.error("❌ Password must be at least 6 characters")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            else:
                # Add new user to database
                st.session_state.users_db[email] = {
                    "password": password,
                    "name": name,
                    "phone": phone,
                    "borrowed_books": []
                }
                st.session_state.users_db[phone] = {
                    "password": password,
                    "name": name,
                    "email": email,
                    "borrowed_books": []
                }
                st.success("✅ Account created successfully! Please login.")
                st.info("Redirecting to login page...")
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown("---")
        if st.button("Already have an account? Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()

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
            
            if st.button("Login with Gmail", use_container_width=True, type="primary"):
                if not email:
                    st.error("❌ Please enter email")
                elif not validate_email(email):
                    st.error("❌ Invalid Gmail format (use @gmail.com)")
                elif email not in st.session_state.users_db:
                    st.error("❌ Email not found in system")
                elif st.session_state.users_db[email]["password"] != password:
                    st.error("❌ Invalid password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_name = st.session_state.users_db[email]["name"]
                    st.session_state.user_phone = st.session_state.users_db[email].get("phone", "N/A")
                    st.success(f"✅ Welcome, {st.session_state.user_name}!")
                    st.rerun()
        
        else:  # Phone Number Login
            phone = st.text_input("📱 Enter Phone Number (10 digits)", placeholder="9876543210")
            password = st.text_input("🔐 Enter Password", type="password")
            
            if st.button("Login with Phone", use_container_width=True, type="primary"):
                if not phone:
                    st.error("❌ Please enter phone number")
                elif not validate_phone(phone):
                    st.error("❌ Invalid phone format (10 digits, starting with 6-9)")
                elif phone not in st.session_state.users_db:
                    st.error("❌ Phone number not registered")
                elif st.session_state.users_db[phone]["password"] != password:
                    st.error("❌ Invalid password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.user_name = st.session_state.users_db[phone]["name"]
                    st.session_state.user_email = st.session_state.users_db[phone].get("email", "N/A")
                    st.success(f"✅ Welcome, {st.session_state.user_name}!")
                    st.rerun()
        
        st.markdown("---")
        if st.button("Create new account? Sign Up", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()
        
        st.markdown("---")
        st.info("📌 Demo Credentials:\n- Email: user1@gmail.com | Pass: pass123\n- Phone: 9876543210 | Pass: pass123")

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
    if st.session_state.user_email and st.session_state.user_email in st.session_state.users_db:
        user_key = st.session_state.user_email
    elif st.session_state.user_phone and st.session_state.user_phone in st.session_state.users_db:
        user_key = st.session_state.user_phone
    else:
        user_key = None
    
    borrowed_book_ids = st.session_state.users_db[user_key].get("borrowed_books", []) if user_key else []
    
    # Tabs for navigation
    tab1, tab2 = st.tabs(["📚 My Borrowed Books", "📖 Available Books in Library"])
    
    with tab1:
        st.subheader("Your Borrowed Books")
        
        if not borrowed_book_ids:
            st.info("ℹ️ You haven't borrowed any books yet.")
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
            st.warning("⚠️ No books match your search criteria.")
        
        st.markdown("---")
