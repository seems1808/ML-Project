import streamlit as st
from database import get_connection


def show_home():

    # ---------------- Session State ----------------

    if "cart" not in st.session_state:
        st.session_state.cart = []

    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None

    if "page" not in st.session_state:
        st.session_state.page = "Home"


    # ---------------- Load Books from Database ----------------

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            author,
            category,
            price,
            rating,
            image,
            description
        FROM books
        ORDER BY title
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    books = []

    for row in rows:

        books.append({

            "id": row[0],
            "title": row[1],
            "author": row[2],
            "category": row[3],
            "price": row[4],
            "rating": row[5],
            "image": row[6],
            "description": row[7]

        })

    # ---------------- Home Banner ----------------

    st.markdown("""
<style>

.title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:#8B4513;
    font-family:'Georgia', serif;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#666666;
    font-style:italic;
    margin-bottom:35px;
}

</style>

<div class="title">
📚 BookNest
</div>

<div class="subtitle">
Your Gateway to Knowledge & Stories
</div>

""", unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1200",
        use_container_width=True
    )

    st.markdown("---")

    # ---------------- Hero ----------------

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown("## 📖 Find Your Next Favorite Book")

        st.write("""
Explore thousands of books from different categories.
Discover best sellers, new arrivals, and timeless classics.
""")

        search = st.text_input(
            "🔍 Search Books",
            placeholder="Search by title or author..."
        )

    with col2:

        st.info("""
### 🎉 Today's Offer

✅ Free Shipping

✅ 10% Discount

✅ Secure Payment
""")

    # ---------------- Search ----------------

    if search:

        search = search.lower()

        books = [

            book

            for book in books

            if search in book["title"].lower()

            or search in book["author"].lower()

        ]

    st.markdown("---")

    # ---------------- Categories ----------------

    st.subheader("📚 Browse Categories")

    categories = ["All"] + sorted(

        list(

            set(

                book["category"]

                for book in books

            )

        )

    )

    selected_category = st.selectbox(

        "Choose Category",

        categories

    )

    if selected_category != "All":

        books = [

            book

            for book in books

            if book["category"] == selected_category

        ]

    st.markdown("---")

    # ---------------- Featured Books ----------------

    st.subheader("🔥 Featured Books")

    if len(books) == 0:

        st.warning("No books found.")

    else:

        for i in range(0, len(books), 3):

            cols = st.columns(3)

            for j in range(3):

                if i + j < len(books):

                    book = books[i + j]

                    with cols[j]:

                        if book["image"]:

                          st.image(
                              book["image"],
                              use_container_width=True
                            )

                        else:

                         st.image(
                              "https://via.placeholder.com/300x450?text=No+Image",
                               use_container_width=True
                          )
                        st.markdown(

                            f"""
<div style="height:70px">
<h4>{book['title']}</h4>
</div>
""",

                            unsafe_allow_html=True

                        )

                        st.caption(book["author"])

                        st.write("⭐" * int(book["rating"]))

                        st.markdown(f"### ₹{book['price']}")

                        if st.button(

                            "📖 View Book",

                            key=f"home_{book['id']}"

                        ):

                            st.session_state.selected_book = book

                            st.session_state.page = "Book Details"

                            st.rerun()

    st.markdown("---")

    # ---------------- Highest Rated Books ----------------

    st.subheader("⭐ Highest Rated Books")

    top_books = sorted(

        books,

        key=lambda x: float(x["rating"]),

        reverse=True

    )

    cols = st.columns(3)

    for i, book in enumerate(top_books[:3]):

     with cols[i]:

        if book["image"]:

            st.image(
                book["image"],
                use_container_width=True
            )

        else:

            st.image(
                "https://via.placeholder.com/300x450?text=No+Image",
                use_container_width=True
            )

        st.markdown(
            f"### {book['title']}"
        )

        st.caption(
            book["author"]
        )

        st.write(
            "⭐" * int(book["rating"])
        )

        st.markdown(
            f"### ₹{book['price']}"
        )

    # ---------------- Why Choose Us ----------------

    st.subheader("⭐ Why Choose BookNest?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success("🚚 Fast Delivery")

    with c2:
        st.success("🔒 Secure Payments")

    with c3:
        st.success("📞 24/7 Customer Support")

    st.markdown("---")

    # ---------------- Footer ----------------

    st.markdown(
        """
<center>

### 📚 BookNest

Your trusted online bookstore.

Made ❤️ for Readers

</center>
""",
        unsafe_allow_html=True
    )
