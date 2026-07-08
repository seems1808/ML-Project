import streamlit as st
from streamlit_option_menu import option_menu

# -------------------- Import Pages --------------------
from views.Home import show_home
from views.Books import show_books
from views.Book_Details import show_book_details
from views.Cart import show_cart
from views.Orders import show_orders
from views.Profile import show_profile
from views.Login import show_login
from views.Register import show_register
from views.Checkout import show_checkout
from views.Admin import show_admin

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="BookNest",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Session State --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "role" not in st.session_state:
    st.session_state.role = "user"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "orders" not in st.session_state:
    st.session_state.orders = []

if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

if "page" not in st.session_state:
    st.session_state.page = "Login"

# -------------------- Sidebar --------------------
with st.sidebar:

    st.markdown("""
<style>

.booknest-title{
    text-align:center;
    font-size:52px;
    font-weight:300;
    color:#5C4033;
    font-family:'Georgia', serif;
    margin-bottom:0px;
    letter-spacing:1px;
}

.booknest-caption{
    text-align:center;
    font-size:20px;
    color:#7D5A50;
    font-style:italic;
    margin-top:-10px;
    margin-bottom:35px;
}

</style>

<div class="booknest-title">
📚 BookNest
</div>

<div class="booknest-caption">
A Nest for Every Reader
</div>

""", unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.success(
            f"👋 Welcome\n\n{st.session_state.current_user['name']}"
        )
        # ---------------- Navigation ----------------
    if st.session_state.logged_in:

        pages = [
            "Home",
            "Books",
            "Cart",
            "Orders",
            "Profile",
            "Checkout"
        ]

        icons = [
            "house",
            "book",
            "cart",
            "bag",
            "person",
            "credit-card"
        ]

        # Show Admin only for admin users
        if st.session_state.role == "admin":
            pages.append("Admin")
            icons.append("gear")

    else:

        pages = [
            "Login",
            "Register"
        ]

        icons = [
            "box-arrow-in-right",
            "person-plus"
        ]

    # Book Details page handling
    if st.session_state.page in pages:
        default_index = pages.index(st.session_state.page)
    else:
        default_index = 0

    menu = option_menu(
        menu_title="Navigation",
        options=pages,
        icons=icons,
        default_index=default_index
    )
    
# -------------------- Update Current Page --------------------
if st.session_state.page != "Book Details":
    st.session_state.page = menu

page = st.session_state.page

# -------------------- Navigation --------------------
if page == "Home":
    show_home()

elif page == "Books":
    show_books()

elif page == "Book Details":
    show_book_details()

elif page == "Cart":
    show_cart()

elif page == "Orders":
    show_orders()

elif page == "Profile":
    show_profile()

elif page == "Login":
    show_login()

elif page == "Register":
    show_register()

elif page == "Checkout":
    show_checkout()

elif page == "Admin":
    if st.session_state.role == "admin":
        show_admin()
    else:
        st.error("❌ Access Denied")