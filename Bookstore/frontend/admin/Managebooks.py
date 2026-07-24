
import streamlit as st
from database import get_connection
from imagekit_config import upload_image


def show_managebooks():

    st.title("📚 BOOK MANAGEMENT")
    st.caption("Add, Search and Manage Books")

    st.markdown("---")

    # ----------------------------------
    # Database Connection
    # ----------------------------------

    conn = get_connection()
    cursor = conn.cursor()

    # ----------------------------------
    # Total Books
    # ----------------------------------

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    st.metric(
        "Total Books",
        total_books
    )

    st.markdown("---")

    # ----------------------------------
    # Search Books
    # ----------------------------------

    search = st.text_input(
        "🔍 Search Book",
        placeholder="Search by title or author..."
    )

    st.markdown("---")

    # ----------------------------------
    # Add New Book
    # ----------------------------------

    st.subheader("➕ Add New Book")

    with st.form("add_book"):

        title = st.text_input("Book Title")

        author = st.text_input("Author")

        category = st.text_input("Category")

        price = st.number_input(
            "Price",
            min_value=0
        )

        rating = st.number_input(
            "Rating",
            min_value=0.0,
            max_value=5.0,
            step=0.1
        )

        image_file = st.file_uploader(
            "Upload Book Image",
            type=["jpg", "jpeg", "png"]
        )

        description = st.text_area(
            "Description"
        )

        submit = st.form_submit_button(
            "Add Book"
        )

        # ----------------------------------
        # Add Book Button
        # ----------------------------------

        if submit:

            if image_file is None:

                st.error(
                    "Please upload a book image."
                )

            else:

                image_url = upload_image(
                    image_file
                )

                cursor.execute(
                    """
                    INSERT INTO books
                    (
                        title,
                        author,
                        category,
                        price,
                        rating,
                        image,
                        description
                    )

                    VALUES
                    (
                        %s,%s,%s,%s,%s,%s,%s
                    )
                    """,
                    (
                        title,
                        author,
                        category,
                        price,
                        rating,
                        image_url,
                        description
                    )
                )

                conn.commit()

                st.success(
                    "Book Added Successfully."
                )

                st.rerun()

    st.markdown("---")

    # ----------------------------------
    # Display Books
    # ----------------------------------

    cursor.execute(
        """
        SELECT
            id,
            title,
            author,
            category,
            price,
            rating,
            image

        FROM books

        ORDER BY id DESC
        """
    )

    books = cursor.fetchall()

    # ----------------------------------
    # Search Filter
    # ----------------------------------

    if search:

        books = [

            book

            for book in books

            if search.lower() in book[1].lower()
            or search.lower() in book[2].lower()

        ]

    # ----------------------------------
    # Show Books
    # ----------------------------------

    st.subheader("📚 All Books")

    if len(books) == 0:

        st.warning(
            "No Books Found."
        )

    else:

        for book in books:

            st.markdown("---")

            st.subheader(
                book[1]
            )

            st.image(
                book[6],
                width=150
            )

            st.write(
                f"Author : {book[2]}"
            )

            st.write(
                f"Category : {book[3]}"
            )

            st.write(
                f"Price : ₹{book[4]}"
            )

            st.write(
                f"Rating : ⭐ {book[5]}"
            )

            # ----------------------------------
            # Edit & Delete Buttons
            # ----------------------------------

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Edit",
                    key=f"edit_{book[0]}"
                ):

                    st.session_state.edit_book_id = book[0]

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{book[0]}"
                ):

                    cursor.execute(
                        """
                        DELETE FROM books
                        WHERE id=%s
                        """,
                        (book[0],)
                    )

                    conn.commit()

                    st.success(
                        "Book Deleted Successfully."
                    )

                    st.rerun()

    # ----------------------------------
    # Edit Book Section
    # ----------------------------------

    if "edit_book_id" in st.session_state:

        book_id = st.session_state.edit_book_id

        cursor.execute(
            """
            SELECT
                title,
                author,
                category,
                price,
                rating,
                description

            FROM books

            WHERE id=%s
            """,
            (book_id,)
        )

        data = cursor.fetchone()

        if data:

            st.markdown("---")

            st.subheader(
                "✏ Edit Book"
            )

            with st.form("edit_book_form"):

                new_title = st.text_input(
                    "Book Title",
                    value=data[0]
                )

                new_author = st.text_input(
                    "Author",
                    value=data[1]
                )

                new_category = st.text_input(
                    "Category",
                    value=data[2]
                )

                new_price = st.number_input(
                    "Price",
                    value=float(data[3])
                )

                new_rating = st.number_input(
                    "Rating",
                    min_value=0.0,
                    max_value=5.0,
                    step=0.1,
                    value=float(data[4])
                )

                new_description = st.text_area(
                    "Description",
                    value=data[5]
                )

                new_image = st.file_uploader(
                    "Upload New Image (Optional)",
                    type=["jpg", "jpeg", "png"]
                )

                update = st.form_submit_button(
                    "Update Book"
                )

                if update:

                    # Update image if uploaded
                    if new_image is not None:

                        image_url = upload_image(
                            new_image
                        )

                        cursor.execute(
                            """
                            UPDATE books

                            SET
                                title=%s,
                                author=%s,
                                category=%s,
                                price=%s,
                                rating=%s,
                                image=%s,
                                description=%s

                            WHERE id=%s
                            """,
                            (
                                new_title,
                                new_author,
                                new_category,
                                new_price,
                                new_rating,
                                image_url,
                                new_description,
                                book_id
                            )
                        )

                    else:

                        cursor.execute(
                            """
                            UPDATE books

                            SET
                                title=%s,
                                author=%s,
                                category=%s,
                                price=%s,
                                rating=%s,
                                description=%s

                            WHERE id=%s
                            """,
                            (
                                new_title,
                                new_author,
                                new_category,
                                new_price,
                                new_rating,
                                new_description,
                                book_id
                            )
                        )

                    conn.commit()

                    del st.session_state.edit_book_id

                    st.success(
                        "Book Updated Successfully."
                    )

                    st.rerun()

    # ----------------------------------
    # Close Connection
    # ----------------------------------

    cursor.close()
    conn.close()
