import streamlit as st
import pandas as pd
from pathlib import Path


def show_books():

    st.title("📚 All Books")
    st.caption("Browse our complete collection")

    # ---------------- Session State ----------------
    if "cart" not in st.session_state:
        st.session_state.cart = []

    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None

    # ---------------- Paths ----------------
    BASE_DIR = Path(__file__).parent.parent
    ASSETS = BASE_DIR / "assets"
    DATA = BASE_DIR / "data"

    # ---------------- Load Dataset ----------------
    df = pd.read_csv(DATA / "books.csv")
    books = df.to_dict(orient="records")

    # ---------------- Search ----------------
    search = st.text_input(
        "🔍 Search Books",
        placeholder="Search by title or author..."
    )

    if search:
        books = [
            book for book in books
            if search.lower() in str(book["title"]).lower()
            or search.lower() in str(book["author"]).lower()
        ]

    # ---------------- Category Filter ----------------
    categories = ["All"] + sorted(df["category"].unique().tolist())

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

            image_path = ASSETS / book["image"]

            st.image(
                image_path,
                use_container_width=True
            )

            st.subheader(book["title"])
            st.caption(book["author"])

            st.write("⭐" * int(book["rating"]))

            st.markdown(f"### ₹{book['price']}")

            col1, col2 = st.columns(2)

            # ---------------- Add to Cart ----------------
            with col1:

                if st.button("🛒 Add", key=f"cart_{book['id']}"):

                    found = False

                    # Check if already in cart
                    for item in st.session_state.cart:
                        if item["id"] == book["id"]:
                            item["quantity"] += 1
                            found = True
                            break

                    # Add new book if not found
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

            # ---------------- View Book ----------------
            with col2:

                if st.button(
                    "📖 View",
                    key=f"view_{book['id']}"
                ):

                    st.session_state.selected_book = book
                    st.session_state.page = "Book Details"
                    st.rerun()

    st.markdown("---")