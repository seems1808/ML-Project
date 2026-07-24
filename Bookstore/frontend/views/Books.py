import streamlit as st
from database import get_connection


def show_books():

    st.title("📚 All Books")
    st.caption("Browse our complete collection")

    # ---------------- Session State ----------------

    if "cart" not in st.session_state:
        st.session_state.cart = []

    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None



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

    # ---------------- Search ----------------

    search = st.text_input(
        "🔍 Search Books",
        placeholder="Search by title or author..."
    )

    if search:

        books = [

            book for book in books

            if search.lower() in book["title"].lower()

            or search.lower() in book["author"].lower()

        ]

    # ---------------- Category Filter ----------------

    categories = ["All"] + sorted(

        list(

            set(

                book["category"]

                for book in books

            )

        )

    )

    category = st.selectbox(

        "📚 Select Category",

        categories

    )

    if category != "All":

        books = [

            book for book in books

            if book["category"] == category

        ]

    st.markdown("---")

    # ---------------- Display Books ----------------

    cols = st.columns(3)

    for index, book in enumerate(books):

        with cols[index % 3]:

            if book["image"]:

             st.image(
                      book["image"],
                      width=200
             )

            else:

             st.image(
                   "https://via.placeholder.com/300x450?text=No+Image",
                    use_container_width=True
             )

            st.subheader(book["title"])

            st.caption(book["author"])

            st.write("⭐" * int(book["rating"]))

            st.markdown(f"### ₹{book['price']}")

            col1, col2 = st.columns(2)

            # ---------------- Add to Cart ----------------

            with col1:

                if st.button(

                    "🛒 Add",

                    key=f"cart_{book['id']}"

                ):

                    found = False

                    for item in st.session_state.cart:

                        if item["id"] == book["id"]:

                            item["quantity"] += 1

                            found = True

                            break

                    if not found:

                        st.session_state.cart.append({

                            "id": book["id"],

                            "title": book["title"],

                            "author": book["author"],

                            "price": int(book["price"]),

                            "quantity": 1

                        })

                    st.success("✅ Book added to cart!")

                    st.rerun()

            # ---------------- View Details ----------------

            with col2:

                if st.button(

                    "📖 View",

                    key=f"view_{book['id']}"

                ):

                    st.session_state.selected_book = book

                    st.session_state.page = "Book Details"

                    st.rerun()

    st.markdown("---")
