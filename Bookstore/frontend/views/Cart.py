import streamlit as st

def show_cart():

    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.title("🛒 Shopping Cart")

    cart = st.session_state.cart

    if len(cart) == 0:
        st.info("🛍️ Your cart is empty.")
        st.write("Go to the Home page and add some books.")
        return

    total = 0

    for i, book in enumerate(cart):

        st.markdown("---")

        col1, col2, col3 = st.columns([4,2,1])

        # ---------------- Book Details ----------------
        with col1:
            st.subheader(book["title"])
            st.write(book["author"])
            st.write(f"Price : ₹{book['price']}")

        # ---------------- Quantity ----------------
        with col2:

            m, q, p = st.columns([1,1,1])

            with m:
                if st.button("➖", key=f"minus_{i}"):

                    if book["quantity"] > 1:
                        book["quantity"] -= 1
                    else:
                        st.session_state.cart.pop(i)

                    st.rerun()

            with q:
                st.markdown(
                    f"<h3 style='text-align:center'>{book['quantity']}</h3>",
                    unsafe_allow_html=True
                )

            with p:
                if st.button("➕", key=f"plus_{i}"):

                    book["quantity"] += 1
                    st.rerun()

        # ---------------- Remove ----------------
        with col3:

            if st.button("❌", key=f"remove_{i}"):

                st.session_state.cart.pop(i)
                st.rerun()

        subtotal = book["price"] * book["quantity"]

        st.write(f"**Subtotal : ₹{subtotal}**")

        total += subtotal

    st.markdown("---")

    st.subheader(f"Grand Total : ₹{total}")

    if st.button("Proceed to Checkout", use_container_width=True):
        st.session_state.page = "Checkout"
        st.rerun()