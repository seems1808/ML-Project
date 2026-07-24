import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# -----------------------------------
# Sender Email (BookNest Gmail)
# -----------------------------------

SENDER_EMAIL = "booknest87@gmail.com"
SENDER_PASSWORD = "emfrhniasvjhjawe"


# -----------------------------------
# Admin Email
# -----------------------------------

ADMIN_EMAIL = "seemammahajan18@gmail.com"


# ===================================
# Send Email to Admin
# ===================================

def send_admin_email(customer_name,
                     customer_email,
                     book_name,
                     total,
                     payment,
                     address,
                     phone):

    try:

        subject = "📚 New Order Received - BookNest"

        body = f"""
A new order has been placed.

---------------------------------------

Customer Name : {customer_name}

Customer Email : {customer_email}

Books Ordered :
{book_name}

Total Amount : ₹{total}

Payment Method : {payment}

Phone Number : {phone}

Address :
{address}

---------------------------------------
"""

        message = MIMEMultipart()

        message["From"] = SENDER_EMAIL
        message["To"] = ADMIN_EMAIL
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            ADMIN_EMAIL,
            message.as_string()
        )

        server.quit()

        st.success("✅ Admin email sent successfully.")

    except Exception as e:

        st.error(f"❌ Admin Email Error: {e}")


# ===================================
# Send Email to User
# ===================================

def send_user_email(customer_name,
                    customer_email,
                    book_name,
                    total,
                    payment):

    try:

        subject = "📚 Your BookNest Order is Confirmed"

        body = f"""
Hello {customer_name},

Thank you for shopping with BookNest.

Your order has been placed successfully.

---------------------------------------

Books Ordered:

{book_name}

---------------------------------------

Total Amount : ₹{total}

Payment Method : {payment}

---------------------------------------

Your order will be delivered soon.

Happy Reading!

Regards,

BookNest Team
"""

        message = MIMEMultipart()

        message["From"] = SENDER_EMAIL
        message["To"] = customer_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            customer_email,
            message.as_string()
        )

        server.quit()

        st.success("✅ User confirmation email sent successfully.")

    except Exception as e:

        st.error(f"❌ User Email Error: {e}")