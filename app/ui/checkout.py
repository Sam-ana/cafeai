import json
from datetime import datetime
from pathlib import Path

import streamlit as st


ORDERS_FILE = Path(
    "data/orders/orders.json"
)


def calculate_total():

    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


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


    orders.append(order)


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


def render_checkout():

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


    if not st.session_state.cart:

        st.warning(
            "Your cart is empty."
        )

        return


    total = calculate_total()


    st.markdown(
        f"""
        ### Order total

        ## NPR {total}
        """
    )


    with st.form("checkout_form"):

        name = st.text_input(
            "Your name"
        )

        phone = st.text_input(
            "Phone number"
        )


        submitted = st.form_submit_button(
            "Place Order ☕"
        )


        if submitted:

            if not name.strip():

                st.error(
                    "Please enter your name."
                )

                return


            if not phone.strip():

                st.error(
                    "Please enter your phone number."
                )

                return


            order = save_order(
                name,
                phone,
                st.session_state.cart,
                total,
            )


            st.success(
                "Your order has been placed successfully! 🎉"
            )


            st.markdown(
                f"""
                ### Thank you, {name}!

                **Order ID:** `{order["order_id"]}`

                **Total:** NPR {total}

                Your CafeAI order has been saved.
                """
            )


            st.session_state.cart = []