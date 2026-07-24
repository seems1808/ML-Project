import streamlit as st
import pandas as pd
from database import get_connection


# ------------------------------------------------
# TOTAL BOOKS
# ------------------------------------------------

def get_total_books():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM books"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    except:

        return 0


# ------------------------------------------------
# TOTAL USERS
# ------------------------------------------------

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


# ------------------------------------------------
# TOTAL ORDERS
# ------------------------------------------------

def get_total_orders():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM orders"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    except:

        return 0


# ------------------------------------------------
# TOTAL REVENUE
# ------------------------------------------------

def get_total_revenue():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT COALESCE(SUM(total),0)
        FROM orders

        """)

        revenue = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return revenue

    except:

        return 0


# ------------------------------------------------
# HIGHEST RATED BOOK
# ------------------------------------------------

def highest_rated_book():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT title
        FROM books
        ORDER BY rating DESC
        LIMIT 1

        """)

        book = cursor.fetchone()

        cursor.close()
        conn.close()

        if book:
            return book[0]

        return "Not Available"

    except:

        return "Not Available"


# ------------------------------------------------
# MOST POPULAR CATEGORY
# ------------------------------------------------

def popular_category():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT category,
        COUNT(*)

        FROM books

        GROUP BY category

        ORDER BY COUNT(*) DESC

        LIMIT 1

        """)

        category = cursor.fetchone()

        cursor.close()
        conn.close()

        if category:
            return category[0]

        return "Not Available"

    except:

        return "Not Available"


# ------------------------------------------------
# AVERAGE RATING
# ------------------------------------------------

def average_rating():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT ROUND(AVG(rating),2)
        FROM books

        """)

        rating = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return rating

    except:

        return 0


# ------------------------------------------------
# TOP BOOKS
# ------------------------------------------------

def top_books():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT title
        FROM books

        ORDER BY rating DESC

        LIMIT 5

        """)

        books = cursor.fetchall()

        cursor.close()
        conn.close()

        return [book[0] for book in books]

    except:

        return []


# ------------------------------------------------
# CATEGORY ANALYTICS
# ------------------------------------------------

def category_statistics():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT category,
        COUNT(*)

        FROM books

        GROUP BY category

        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if len(rows) == 0:
            return []

        categories = {}
        for row in rows:
            categories[row[0]] = row[1]

        return pd.Series(categories)

    except:

        return []


# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------

def show_dashboard():

    st.title("📚 BOOKNEST AI DASHBOARD")

    st.caption(
        "AI Powered Book Recommendation System"
    )

    st.markdown("---")


    # ---------------------------------------

    st.subheader("Today's Statistics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Books",
            get_total_books()
        )

    with col2:

        st.metric(
            "Total Users",
            get_total_users()
        )


    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "Total Orders",
            get_total_orders()
        )

    with col4:

        st.metric(
            "Revenue",
            f"₹{get_total_revenue()}"
        )

    st.markdown("---")


    # ---------------------------------------

    st.subheader("AI Insights")

    st.success(
        f"Highest Rated Book : {highest_rated_book()}"
    )

    st.info(
        f"Most Popular Category : {popular_category()}"
    )

    st.warning(
        f"Average Rating : {average_rating()}"
    )

    st.markdown("---")


    # ---------------------------------------

    st.subheader("AI ENGINE")

    st.success(
        "Recommendation Model : Random Forest"
    )

    st.write(
        "Prediction Method : predict_proba()"
    )

    st.write(
        "Recommendation Type : Top 3 Books"
    )

    st.write(
        "Features Used :"
    )

    st.write("- Category")
    st.write("- Author")
    st.write("- Price")
    st.write("- Rating")

    st.markdown("---")


    # ---------------------------------------

    st.subheader("LIVE CATEGORY ANALYTICS")

    stats = category_statistics()

    if len(stats) > 0:

        st.bar_chart(stats)

    st.markdown("---")


    # ---------------------------------------

    st.subheader("TOP RECOMMENDED BOOKS")

    books = top_books()

    for book in books:

        st.write(f"📖 {book}")

    st.markdown("---")


    # ---------------------------------------

    st.subheader("RECOMMENDATION FLOW")

    st.code("""

Select Book
      ↓
Random Forest
      ↓
predict_proba()
      ↓
Probability Score
      ↓
Top 3 Books
      ↓
Display Results

""")

    st.markdown("---")


    # ---------------------------------------

    st.subheader("TODAY'S AI REPORT")

    st.write(
        f"Dataset Size : {get_total_books()} Books"
    )

    st.write(
        f"Total Users : {get_total_users()}"
    )

    st.write(
        f"Average Rating : {average_rating()}"
    )

    st.write(
        "Machine Learning Model : Random Forest"
    )

    st.write(
        "Recommendation System : Top 3 Books"
    )

    st.write(
        "Prediction Method : predict_proba()"
    )

    st.markdown("---")


    st.success(
        "BookNest uses an AI powered Random Forest "
        "recommendation system to recommend books "
        "to its users."
    )
