import streamlit as st
import pandas as pd
from database import get_connection


# --------------------------------------
# TOTAL ORDERS
# --------------------------------------

def get_total_orders():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM orders"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    except:

        return 0


# --------------------------------------
# TOTAL REVENUE
# --------------------------------------

def get_total_revenue():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COALESCE(SUM(total),0)
            FROM orders
            """
        )

        revenue = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return revenue

    except:

        return 0


# --------------------------------------
# LOAD ALL ORDERS
# --------------------------------------

def load_orders():

    conn = get_connection()

    query = """
    SELECT

        id,
        customer_name,
        book_name,
        total,
        payment,
        address,
        phone,
        order_date,
        transaction_id

    FROM orders

    ORDER BY order_date DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# --------------------------------------
# SHOW ORDERS PAGE
# --------------------------------------

def show_admin_orders():

    st.title("📦 ALL CUSTOMER ORDERS")

    st.caption(
        "Manage and View All Orders"
    )

    st.markdown("---")


    # ----------------------------------
    # ORDER STATISTICS
    # ----------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Orders",
             get_total_orders()
        )

    with col2:

        st.metric(
            "Total Revenue",
            f"₹{get_total_revenue()}"
        )


    st.markdown("---")


    # ----------------------------------
    # SEARCH BOX
    # ----------------------------------

    search = st.text_input(
        "🔍 Search by Customer or Book Name"
    )


    # ----------------------------------
    # PAYMENT FILTER
    # ----------------------------------

    payment_filter = st.selectbox(

        "Payment Method",

        [
            "All",
            "Cash on Delivery",
            "UPI",
            "Credit Card",
            "Debit Card"
        ]

    )


    # ----------------------------------
    # LOAD ORDERS
    # ----------------------------------

    df = load_orders()


    # ----------------------------------
    # SEARCH FILTER
    # ----------------------------------

    if search:

        df = df[

            df["customer_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )

            |

            df["book_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )

        ]


    # ----------------------------------
    # PAYMENT FILTER
    # ----------------------------------

    if payment_filter != "All":

        df = df[

            df["payment"] == payment_filter

        ]


    # ----------------------------------
    # NO ORDERS
    # ----------------------------------

    if df.empty:

        st.warning(
            "No Orders Found."
        )

        return


    # ----------------------------------
    # DISPLAY ORDERS
    # ----------------------------------

    for index, row in df.iterrows():

        st.markdown("---")

        st.subheader(
            f"📦 Order #{row['id']}"
        )

        st.write(
            f"👤 Customer Name : {row['customer_name']}"
        )

        st.write(
            f"📚 Book Name : {row['book_name']}"
        )

        st.write(
            f"💰 Total Amount : ₹{row['total']}"
        )

        st.write(
            f"💳 Payment Method : {row['payment']}"
        )

        st.write(
            f"🏠 Address : {row['address']}"
        )

        st.write(
            f"📞 Phone Number : {row['phone']}"
        )

        st.write(
            f"🆔 Transaction ID : {row['transaction_id']}"
        )

        st.write(
            f"📅 Order Date : {row['order_date']}"
        )
