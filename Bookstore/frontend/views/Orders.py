import streamlit as st
from database import get_connection


def show_orders():

    st.title("📦 My Orders")

    if not st.session_state.logged_in:
        st.warning("Please login to view your orders.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            customer_name,
            book_name,
            total,
            payment,
            address,
            phone,
            order_date
        FROM orders
        WHERE user_id = %s
        ORDER BY order_date DESC
        """,
        (st.session_state.current_user["id"],)
    )

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    if not orders:
        st.info("📭 No orders placed yet.")
        return
    total_orders = len(orders)
    for i, order in enumerate(orders):
        st.markdown("---")

        st.subheader(f"📦 Order #{total_orders - i}")

        st.write(f"👤 **Customer:** {order[1]}")
        st.write(f"📚 **Book(s):** {order[2]}")
        st.write(f"💰 **Total:** ₹{order[3]}")
        st.write(f"💳 **Payment:** {order[4]}")
        st.write(f"🏠 **Address:** {order[5]}")
        st.write(f"📞 **Phone:** {order[6]}")
        st.write(f"📅 **Order Date:** {order[7]}")