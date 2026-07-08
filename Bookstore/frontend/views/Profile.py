import streamlit as st
from database import get_connection


def show_profile():

    st.markdown(
        """
        <h1 style='text-align:center;'>👤 My Profile</h1>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Login Check ----------------
    if (
        "logged_in" not in st.session_state
        or not st.session_state.logged_in
    ):
        st.warning("Please Login First")
        return

    user = st.session_state.current_user

    # ---------------- Count Orders from PostgreSQL ----------------
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE user_id=%s
        """,
        (user["id"],)
    )

    order_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    # ---------------- Personal Information ----------------
    st.markdown("## Personal Information")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=170
        )

    with col2:
        st.write(f"## 👤 {user['name']}")
        st.write(f"📧 **Email:** {user['email']}")
        st.write(f"📱 **Phone:** {user['phone']}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📦 Orders", order_count)

    with col2:
        cart_count = sum(
            item["quantity"] for item in st.session_state.get("cart", [])
        )
        st.metric("🛒 Books in Cart", cart_count)

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.role = "user"
        st.session_state.page = "Login"

        st.success("Logged Out Successfully!")
        st.rerun()