import streamlit as st
import pandas as pd
from database import get_connection


# ----------------------------------
# Total Users
# ----------------------------------

def get_total_users():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    except Exception:
        return 0


# ----------------------------------
# Get Users Data
# ----------------------------------

def get_users():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
        id,
        name,
        email,
        is_admin
        FROM users
        ORDER BY id
        """

        cursor.execute(query)

        users = cursor.fetchall()

        cursor.close()
        conn.close()

        df = pd.DataFrame(
            users,
            columns=[
                "Id",
                "Name",
                "Email",
                "is_admin"
            ]
        )

        return df

    except Exception as e:

        print(e)
        return pd.DataFrame()


# ----------------------------------
# Search Users
# ----------------------------------

def search_users(df, keyword):

    if keyword == "":
        return df

    keyword = keyword.lower()

    return df[

        (df["Name"].str.lower().str.contains(keyword))
        |
        (df["Email"].str.lower().str.contains(keyword))

    ]


# ----------------------------------
# Filter Users
# ----------------------------------

def filter_role(df, role):

    if role == "All":
        return df

    elif role == "Admin":
        return df[df["is_admin"] == True]

    elif role == "User":
        return df[df["is_admin"] == False]

    return df


# ----------------------------------
# Registration Statistics
# ----------------------------------

def registration_statistics(df):

    total_users = len(df)

    admins = len(
        df[df["is_admin"] == True]
    )

    users = len(
        df[df["is_admin"] == False]
    )

    return total_users, users, admins


# ----------------------------------
# Show Users Page
# ----------------------------------

def show_users():

    st.title(
        "👥 USERS MANAGEMENT"
    )

    st.caption(
        "BookNest AI User Analytics"
    )

    st.markdown("---")


    # Total Users

    total = get_total_users()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Users",
            total
        )

    with col2:

        st.metric(
            "Registered Accounts",
            total
        )

    st.markdown("---")


    # Get Data

    df = get_users()

    if df.empty:

        st.warning(
            "No Users Found."
        )

        return


    # Search

    st.subheader(
        "Search Users"
    )

    keyword = st.text_input(
        "Search by Name or Email"
    )


    # Filter

    role = st.selectbox(

        "Filter by Role",

        [
            "All",
            "Admin",
            "User"
        ]

    )


    # Apply Search

    df = search_users(
        df,
        keyword
    )


    # Apply Filter

    df = filter_role(
        df,
        role
    )


    st.markdown("---")


    # Registered Users Table

    st.subheader(
        "Registered Users"
    )


    # Create a display dataframe

    display_df = df.copy()

    display_df["is_admin"] = display_df["is_admin"].apply(

        lambda x: "Admin" if x else "User"

    )


    st.dataframe(
        display_df,
        width="stretch"
    )

    st.markdown("---")


    # Registration Statistics

    st.subheader(
        "Registration Statistics"
    )

    total_users, users, admins = (

        registration_statistics(df)

    )


    col3, col4, col5 = st.columns(3)

    with col3:

        st.metric(
            "Total",
            total_users
        )

    with col4:

        st.metric(
            "Users",
            users
        )

    with col5:

        st.metric(
            "Admins",
            admins
        )

    st.markdown("---")


    # Role Analytics

    st.subheader(
        "Role Analytics"
    )


    role_chart = display_df["is_admin"].value_counts()

    st.bar_chart(
        role_chart
    )


    st.markdown("---")


    st.success(

        "BookNest AI User Management System is connected with Neon PostgreSQL Database."

    )
