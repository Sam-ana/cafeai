import json
from datetime import datetime
from pathlib import Path

import streamlit as st


# ============================================================
# ORDERS FILE
# ============================================================

ORDERS_FILE = Path(
    "data/orders/orders.json"
)


# ============================================================
# CALCULATE TOTAL
# ============================================================

def calculate_total():

    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


# ============================================================
# SAVE ORDER
# ============================================================

def save_order(
    customer_name,
    phone,
    items,
    total,
):

    ORDERS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # LOAD EXISTING ORDERS
    # --------------------------------------------------------

    if ORDERS_FILE.exists():

        try:

            with open(
                ORDERS_FILE,
                "r",
                encoding="utf-8",
            ) as file:

                orders = json.load(file)

        except json.JSONDecodeError:

            orders = []

    else:

        orders = []

    # --------------------------------------------------------
    # CREATE ORDER
    # --------------------------------------------------------

    order = {

        "order_id":
            f"CAFE-{datetime.now().strftime('%Y%m%d%H%M%S')}",

        "customer_name":
            customer_name,

        "phone":
            phone,

        "items":
            items,

        "total":
            total,

        "created_at":
            datetime.now().isoformat(),
    }

    # --------------------------------------------------------
    # ADD ORDER
    # --------------------------------------------------------

    orders.append(order)

    # --------------------------------------------------------
    # SAVE TO JSON
    # --------------------------------------------------------

    with open(
        ORDERS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            orders,
            file,
            indent=4,
        )

    return order


# ============================================================
# CHECKOUT PAGE
# ============================================================

def render_checkout():

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-heading">

            <div class="eyebrow">
                CHECKOUT
            </div>

            <h2>
                Complete your order.
            </h2>

            <p>
                Almost there. Let's prepare your order.
            </p>

        </div>
        """
    )

    # --------------------------------------------------------
    # EMPTY CART CHECK
    # --------------------------------------------------------

    if not st.session_state.cart:

        st.warning(
            "Your cart is empty."
        )

        return

    # --------------------------------------------------------
    # CALCULATE TOTAL
    # --------------------------------------------------------

    total = calculate_total()

    # --------------------------------------------------------
    # ORDER TOTAL
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="cart-total">

            <span>
                Order Total
            </span>

            <strong>
                NPR {total}
            </strong>

        </div>
        """
    )

    # --------------------------------------------------------
    # CHECKOUT FORM
    # --------------------------------------------------------

    with st.form("checkout_form"):

        name = st.text_input(
            "Your name",
            placeholder="Enter your name",
        )

        phone = st.text_input(
            "Phone number",
            placeholder="Enter your phone number",
        )

        submitted = st.form_submit_button(
            "Place Order ☕",
            use_container_width=True,
        )

        # ----------------------------------------------------
        # SUBMIT ORDER
        # ----------------------------------------------------

        if submitted:

            # -----------------------------------------------
            # VALIDATE NAME
            # -----------------------------------------------

            if not name.strip():

                st.error(
                    "Please enter your name."
                )

                return

            # -----------------------------------------------
            # VALIDATE PHONE
            # -----------------------------------------------

            if not phone.strip():

                st.error(
                    "Please enter your phone number."
                )

                return

            # -----------------------------------------------
            # SAVE ORDER
            # -----------------------------------------------

            order = save_order(
                name,
                phone,
                st.session_state.cart,
                total,
            )

            # -----------------------------------------------
            # SUCCESS MESSAGE
            # -----------------------------------------------

            st.success(
                "Your order has been placed successfully! 🎉"
            )

            # -----------------------------------------------
            # ORDER CONFIRMATION
            # -----------------------------------------------

            st.html(
                f"""
                <div class="section-heading">

                    <div class="eyebrow">
                        GRAZIE
                    </div>

                    <h2>
                        Thank you, {name}!
                    </h2>

                    <p>
                        Your CafeAI order has been saved.
                    </p>

                    <p>
                        <strong>
                            Order ID:
                        </strong>
                        {order["order_id"]}
                    </p>

                    <p>
                        <strong>
                            Total:
                        </strong>
                        NPR {total}
                    </p>

                </div>
                """
            )

            # -----------------------------------------------
            # CLEAR CART
            # -----------------------------------------------

            st.session_state.cart = []
