import streamlit as st

from app.ui.home import render_home
from app.ui.menu import render_menu
from app.ui.barista import render_barista
from app.ui.cart import render_cart
from app.ui.checkout import render_checkout


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CafeAI",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    with open(
        "assets/css/style.css",
        "r",
        encoding="utf-8"
    ) as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        ☕ CafeAI
    </div>

    <div class="sidebar-subtitle">
        Your AI-powered café
    </div>
    """,
    unsafe_allow_html=True,
)


page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Menu",
        "AI Barista",
        "Cart",
        "Checkout",
    ],
    index=[
        "Home",
        "Menu",
        "AI Barista",
        "Cart",
        "Checkout",
    ].index(st.session_state.page),
)


st.session_state.page = page


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Home":
    render_home()

elif page == "Menu":
    render_menu()

elif page == "AI Barista":
    render_barista()

elif page == "Cart":
    render_cart()

elif page == "Checkout":
    render_checkout()