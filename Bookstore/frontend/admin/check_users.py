import streamlit as st
from database import get_connection


def check_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    st.write(data)

    cursor.close()
    conn.close()


check_users()
