import streamlit as st

from app.menu.loader import load_menu


# ============================================================
# MENU
# ============================================================

MENU = load_menu()


# ============================================================
# IMAGE MAP
# ============================================================

MENU_IMAGES = {

    "espresso":
        "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=900&q=85",

    "americano":
        "https://images.unsplash.com/photo-1494314671902-399b18174975?auto=format&fit=crop&w=900&q=85",

    "cafe-latte":
        "https://images.unsplash.com/photo-1561882468-9110e03e0f78?auto=format&fit=crop&w=900&q=85",

    "cappuccino":
        "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=900&q=85",

    "mocha":
        "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?auto=format&fit=crop&w=900&q=85",

    "iced-latte":
        "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=85",

    "iced-americano":
        "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=85",

    "cold-brew":
        "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=900&q=85",

    "chocolate-frappe":
        "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=85",

    "masala-tea":
        "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?auto=format&fit=crop&w=900&q=85",

    "green-tea":
        "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=85",

    "lemon-tea":
        "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=85",

    "chocolate-cake":
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=85",

    "croissant":
        "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=85",

    "brownie":
        "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?auto=format&fit=crop&w=900&q=85",

    "sandwich":
        "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=85",
}


# ============================================================
# ADD TO CART
# ============================================================

def add_to_cart(item):

    cart = st.session_state.cart

    for cart_item in cart:

        if cart_item["id"] == item["id"]:

            cart_item["quantity"] += 1

            return

    cart.append(
        {
            "id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "quantity": 1,
        }
    )


# ============================================================
# PAGE
# ============================================================

def render_menu():

    st.markdown(
        """
        <div class="section-heading">

            <div class="eyebrow">
                IL MENU
            </div>

            <h2>
                Our Menu
            </h2>

            <p>
                Italian-inspired coffee, refreshing drinks,
                tea and delicious treats.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------------

    categories = [
        "All",
        "Coffee",
        "Cold Drinks",
        "Tea",
        "Snacks",
    ]

    selected_category = st.selectbox(
        "Choose a category",
        categories,
    )


    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    if selected_category == "All":

        filtered_menu = MENU

    else:

        filtered_menu = [
            item
            for item in MENU
            if item["category"] == selected_category
        ]


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    for start in range(
        0,
        len(filtered_menu),
        3
    ):

        columns = st.columns(3)

        row_items = filtered_menu[
            start:start + 3
        ]

        for column, item in zip(
            columns,
            row_items
        ):

            with column:

                image = MENU_IMAGES.get(
                    item["id"],
                    "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"
                    "?auto=format&fit=crop&w=900&q=85",
                )

                st.markdown(
                    f"""
                    <div class="product-card">

                        <img
                            src="{image}"
                            class="product-image"
                        />

                        <div class="product-content">

                            <div class="product-category">
                                {item["category"]}
                            </div>

                            <h3>
                                {item["name"]}
                            </h3>

                            <p>
                                {item["description"]}
                            </p>

                            <div class="product-price">
                                NPR {item["price"]}
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Add to Cart",
                    key=f"add_{item['id']}",
                    use_container_width=True,
                ):

                    add_to_cart(item)

                    st.success(
                        f"{item['name']} added to your cart."
                    )