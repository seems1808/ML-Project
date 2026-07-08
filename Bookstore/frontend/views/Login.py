import streamlit as st
from database import get_connection


def show_login():

    st.markdown(
        """
        <h1 style='text-align:center;'>🔐 Welcome Back</h1>
        <h4 style='text-align:center;color:gray;'>
        Login to continue shopping at BookNest
        </h4>
        """,
        unsafe_allow_html=True
    )

    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

    st.write("")

    if st.button("Login", use_container_width=True):

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, email, phone, is_admin
                FROM users
                WHERE email = %s
                AND password = %s
            """, (email, password))

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:

                st.session_state.logged_in = True

                st.session_state.current_user = {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "phone": user[3]
                }

                # Check if Admin
                if user[4]:

                    st.session_state.role = "admin"

                    st.success("✅ Welcome Admin!")

                    st.session_state.page = "Admin"

                else:

                    st.session_state.role = "user"

                    st.success("✅ Login Successful!")

                    st.session_state.page = "Home"

                st.rerun()

            else:

                st.error("❌ Invalid Email or Password")

        except Exception as e:

            st.error(f"Database Error: {e}")

    st.markdown("---")

    st.write("Don't have an account?")

    if st.button("📝 Register Now", use_container_width=True):

        st.session_state.page = "Register"
        st.rerun()