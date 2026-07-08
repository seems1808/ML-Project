import streamlit as st
from database import get_connection


def show_checkout():

    st.title("💳 Checkout")

    # ---------------- Login Check ----------------
    if not st.session_state.logged_in:
        st.warning("🔒 Please login first.")
        if st.button("Login"):
            st.session_state.page = "Login"
            st.rerun()
        return

    if "cart" not in st.session_state:
        st.session_state.cart = []

    cart = st.session_state.cart

    if len(cart) == 0:
        st.warning("🛒 Your cart is empty.")
        return

    # ---------------- Total ----------------
    total = sum(book["price"] * book["quantity"] for book in cart)

    st.subheader("🛍 Order Summary")

    for book in cart:
        st.write(
            f"📚 {book['title']} "
            f"(Qty: {book['quantity']}) "
            f"₹{book['price'] * book['quantity']}"
        )

    st.markdown("---")
    st.success(f"💰 Total Amount : ₹{total}")

    # ---------------- Shipping ----------------
    st.subheader("🚚 Shipping Details")

    name = st.text_input(
        "Full Name",
        value=st.session_state.current_user["name"]
    )

    address = st.text_area("Address")

    phone = st.text_input(
        "Phone Number",
        value=st.session_state.current_user["phone"]
    )

    payment = st.selectbox(
        "Payment Method",
        [
            "Cash on Delivery",
            "UPI"
        ]
    )

    # ---------------- UPI Payment ----------------
    payment_done = True
    transaction_id = ""

    if payment == "UPI":
        payment_done = False

        st.subheader("📱 UPI Payment")
        st.info("UPI ID : booknest@upi")

        st.image(
            "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=upi://pay?pa=booknest@upi&pn=BookNest&am="
            + str(total),
            width=250
        )

        st.success("Scan the QR code using Google Pay, PhonePe or Paytm.")

        transaction_id = st.text_input("Enter UPI Transaction ID")

        if transaction_id:
            payment_done = True

    # ---------------- Place Order ----------------
    if st.button("✅ Place Order", use_container_width=True):

        if payment == "UPI" and not payment_done:
            st.error("Please complete the UPI payment first.")
            return

        if not address:
            st.error("Please enter your address.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            book_names = ", ".join(book["title"] for book in cart)

            # ---------------- Insert Order ----------------
            cursor.execute(
                """
                INSERT INTO orders
                (user_id, customer_name, book_name, total, payment, transaction_id, address, phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    st.session_state.current_user["id"],
                    name,
                    book_names,
                    total,
                    payment,
                    transaction_id,
                    address,
                    phone
                )
            )

            order_id = cursor.fetchone()[0]

            # ---------------- Insert Order Items ----------------
            for book in cart:
                cursor.execute(
                    """
                    INSERT INTO order_items
                    (order_id, book_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order_id,
                        book["id"],
                        book["quantity"],
                        book["price"]
                    )
                )

            conn.commit()

            st.session_state.cart = []
            st.success("🎉 Order Placed Successfully!")
            st.session_state.page = "Orders"
            st.rerun()

        except Exception as e:
            conn.rollback()
            st.error(f"Database Error: {e}")

        finally:
            cursor.close()
            conn.close()

