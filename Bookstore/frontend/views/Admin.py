import streamlit as st
import pandas as pd

from database import get_connection
   

def show_admin():

    st.title("🛠 Admin Panel")

    conn = get_connection()
    cur = conn.cursor()

    # ---------------- Add Book ----------------

    st.subheader("➕ Add New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    category = st.selectbox(
        "Category",
        [
            "Programming",
            "History",
            "Biography",
            "Fantasy",
            "Fiction",
            "Science",
            "Business"
        ]
    )

    price = st.number_input("Price", min_value=1)

    rating = st.slider("Rating", 1, 5)

    image = st.text_input("Image Name")

    description = st.text_area("Description")

    if st.button("Add Book"):

        cur.execute("""
        INSERT INTO books
        (title,author,category,price,rating,image,description)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            title,
            author,
            category,
            price,
            rating,
            image,
            description
        ))

        conn.commit()

        st.success("Book Added Successfully!")

        st.rerun()

    st.markdown("---")

    # ---------------- Show Books ----------------

    st.subheader("📚 All Books")

    df = pd.read_sql("SELECT * FROM books ORDER BY id", conn)

    for i, row in df.iterrows():

        col1, col2, col3 = st.columns([5,1,1])

        with col1:

            st.write(f"**{row['title']}**")
            st.caption(row["author"])

        with col2:

            if st.button(
                "✏ Edit",
                key=f"edit{row['id']}"
            ):

                st.session_state.edit_book = row["id"]

        with col3:

            if st.button(
                "❌ Delete",
                key=f"delete{row['id']}"
            ):

                cur.execute(
                    "DELETE FROM books WHERE id=%s",
                    (row["id"],)
                )

                conn.commit()

                st.success("Book Deleted")

                st.rerun()

    # ---------------- Edit ----------------

    if "edit_book" in st.session_state:

        book_id = st.session_state.edit_book

        book = pd.read_sql(
            f"SELECT * FROM books WHERE id={book_id}",
            conn
        ).iloc[0]

        st.markdown("---")
        st.subheader("✏ Edit Book")

        new_title = st.text_input(
            "Title",
            value=book["title"]
        )

        new_price = st.number_input(
            "Price",
            value=int(book["price"])
        )

        if st.button("Update Book"):

            cur.execute("""
            UPDATE books
            SET title=%s,
                price=%s
            WHERE id=%s
            """,
            (
                new_title,
                new_price,
                book_id
            ))

            conn.commit()

            del st.session_state.edit_book

            st.success("Book Updated")

            st.rerun()

    cur.close()
    conn.close()