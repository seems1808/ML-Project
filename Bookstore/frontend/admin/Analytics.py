import streamlit as st
import pandas as pd
from database import get_connection


# ---------------------------------
# Total Users
# ---------------------------------

def get_total_users():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    except:
        return 0


# ---------------------------------
# Total Books
# ---------------------------------

def get_total_books():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM books"
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# ---------------------------------
# Average Price
# ---------------------------------

def get_average_price():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(price) FROM books"
    )

    avg = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if avg is None:
        return 0

    return round(avg, 2)


# ---------------------------------
# Total Categories
# ---------------------------------

def get_total_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(DISTINCT category)
        FROM books
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# ---------------------------------
# Load Books Data
# ---------------------------------

def load_books():

    conn = get_connection()

    query = """
    SELECT
        title,
        author,
        category,
        price,
        rating
    FROM books
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# ---------------------------------
# Show Analytics Page
# ---------------------------------

def show_analytics():

    st.title(
        "📊 BOOKSTORE ANALYTICS"
    )

    st.caption(
        "BookNest AI Analytics Dashboard"
    )

    st.markdown("---")

    # ====================================
    # Metrics
    # ====================================

    total_books = get_total_books()
    total_users = get_total_users()
    avg_price = get_average_price()
    categories = get_total_categories()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Books",
            total_books
        )

    with col2:

        st.metric(
            "Total Users",
            total_users
        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "Average Price",
            f"₹{avg_price}"
        )

    with col4:

        st.metric(
            "Categories",
            categories
        )

    st.markdown("---")

    # ====================================
    # Load Books Data
    # ====================================

    df = load_books()

    # If no books are present

    if df.empty:

        st.warning(
            "No books available."
        )

        return

    # ====================================
    # Category Analytics
    # ====================================

    st.subheader(
        "Books Category Analytics"
    )

    category_chart = (

        df["category"]
        .value_counts()

    )

    st.bar_chart(
        category_chart
    )

    st.markdown("---")

    # ====================================
    # Price Analytics
    # ====================================

    st.subheader(
        "Book Price Analytics"
    )

    st.line_chart(
        df["price"]
    )

    st.markdown("---")

    # ====================================
    # Top Rated Books
    # ====================================

    st.subheader(
        "Top Rated Books"
    )

    top_books = (

        df[
            [
                "title",
                "author",
                "rating",
                "price"
            ]
        ]

        .sort_values(
            by="rating",
            ascending=False
        )

    )

    st.dataframe(
        top_books,
        use_container_width=True
    )

    st.markdown("---")

    # ====================================
    # Most Expensive Books
    # ====================================

    st.subheader(
        "Most Expensive Books"
    )

    expensive_books = (

        df[
            [
                "title",
                "price"
            ]
        ]

        .sort_values(
            by="price",
            ascending=False
        )

    )

    st.dataframe(
        expensive_books,
        use_container_width=True
    )

    st.markdown("---")
