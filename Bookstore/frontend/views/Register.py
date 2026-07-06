import streamlit as st
from database import get_connection


def show_register():

    st.markdown(
        """
        <h1 style='text-align:center;'>📝 Create Account</h1>
        <h4 style='text-align:center;color:gray;'>
        Join BookNest and start your reading journey
        </h4>
        """,
        unsafe_allow_html=True
    )

    with st.form("register_form"):

        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email")
        phone = st.text_input("📱 Phone Number")
        password = st.text_input("🔒 Password", type="password")
        confirm = st.text_input("🔒 Confirm Password", type="password")

        submit = st.form_submit_button(
            "📝 Register",
            use_container_width=True
        )

    if submit:

        if not name or not email or not phone or not password or not confirm:

            st.warning("⚠️ Please fill all required fields.")

        elif password != confirm:

            st.error("❌ Passwords do not match!")

        else:

            conn = get_connection()
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute(
                "SELECT * FROM users WHERE email=%s",
                (email,)
            )

            existing = cursor.fetchone()

            if existing:

                st.error("❌ Email already exists!")

            else:

                cursor.execute(
                    """
                    INSERT INTO users
                    (name,email,password,is_admin,phone)
                    VALUES(%s,%s,%s,%s,%s)
                    """,
                    (
                        name,
                        email,
                        password,
                        False,
                        phone
                    )
                )

                conn.commit()

                st.success("🎉 Registration Successful!")

                st.session_state.page = "Login"

                cursor.close()
                conn.close()

                st.rerun()

            cursor.close()
            conn.close()

    st.markdown("---")

    st.write("Already have an account?")

    if st.button("🔐 Login Now", use_container_width=True):

        st.session_state.page = "Login"
        st.rerun()