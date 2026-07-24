import streamlit as st
from models.recommendation import recommend_books



def show_book_details():

    # ---------------- Session State ----------------
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None

    if "cart" not in st.session_state:
        st.session_state.cart = []

    if st.session_state.selected_book is None:
        st.warning("No book selected.")
        return

    selected = st.session_state.selected_book

    # ---------------- Navigation Buttons ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back to Books"):
            st.session_state.page = "Books"
            st.rerun()

    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # ---------------- Book Details ----------------
    st.title("📖 Book Details")
    if selected["image"]:

     st.image(
        selected["image"],
        width=250
     )

    else:

     st.image(
        "https://via.placeholder.com/300x450?text=No+Image",
        width=250
     )
    st.subheader(selected["title"])

    st.write("**Author:**", selected["author"])
    st.write("**Category:**", selected["category"])
    st.write(f"**Price:** ₹{selected['price']}")
    st.write("**Description:**")
    st.write(selected["description"])
    st.write("⭐" * int(selected["rating"]))

    st.markdown("---")

    # ---------------- Add to Cart ----------------
    if st.button("🛒 Add to Cart", use_container_width=True):

        found = False

        for item in st.session_state.cart:
            if item["id"] == selected["id"]:
                item["quantity"] += 1
                found = True
                break

        if not found:
            st.session_state.cart.append({
                "id": selected["id"],
                "title": selected["title"],
                "author": selected["author"],
                "price": int(selected["price"]),
                "quantity": 1
            })

        st.success("✅ Book added to cart!")
        st.rerun()

    st.markdown("---")

    # ---------------- Recommended Books ----------------
    st.header("🤖 Recommended Books")

    recommendations = recommend_books(selected["title"])

    if len(recommendations) == 0:
        st.info("No recommendations available.")

    else:

        cols = st.columns(3)

        for i, book in enumerate(recommendations):

            with cols[i % 3]:
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

                st.markdown(f"### {book['title']}")
                st.caption(book["author"])

                st.write("⭐" * int(book["rating"]))
                st.markdown(f"### ₹{book['price']}")

                if st.button("View", key=f"recommend_{book['id']}"):
                    st.session_state.selected_book = book
                    st.rerun()