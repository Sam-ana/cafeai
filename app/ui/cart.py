import streamlit as st


# ============================================================
# CALCULATE CART TOTAL
# ============================================================

def calculate_total():

    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


# ============================================================
# RENDER CART
# ============================================================

def render_cart():

    # --------------------------------------------------------
    # CART HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-heading">

            <div class="eyebrow">
                IL TUO ORDINE
            </div>

            <h2>
                Your Cart
            </h2>

            <p>
                Review your selected items before checkout.
            </p>

        </div>
        """
    )

    # --------------------------------------------------------
    # GET CART
    # --------------------------------------------------------

    cart = st.session_state.cart

    # --------------------------------------------------------
    # EMPTY CART
    # --------------------------------------------------------

    if not cart:

        st.info(
            "Your cart is empty. "
            "Visit the Menu to add something delicious. ☕"
        )

        return

    # --------------------------------------------------------
    # CART ITEMS
    # --------------------------------------------------------

    for index, item in enumerate(cart):

        col1, col2, col3, col4 = st.columns(
            [4, 1, 1, 1]
        )

        # ----------------------------------------------------
        # ITEM NAME + PRICE
        # ----------------------------------------------------

        with col1:

            st.markdown(
                f"""
                **{item["name"]}**

                NPR {item["price"]} each
                """
            )

        # ----------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------

        with col2:

            st.write(
                f"Qty: {item['quantity']}"
            )

        # ----------------------------------------------------
        # SUBTOTAL
        # ----------------------------------------------------

        with col3:

            subtotal = (
                item["price"]
                * item["quantity"]
            )

            st.write(
                f"NPR {subtotal}"
            )

        # ----------------------------------------------------
        # REMOVE BUTTON
        # ----------------------------------------------------

        with col4:

            if st.button(
                "Remove",
                key=f"remove_{index}",
            ):

                st.session_state.cart.pop(
                    index
                )

                st.rerun()

    # --------------------------------------------------------
    # DIVIDER
    # --------------------------------------------------------

    st.divider()

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    total = calculate_total()

    st.html(
        f"""
        <div class="cart-total">

            <span>
                Total
            </span>

            <strong>
                NPR {total}
            </strong>

        </div>
        """
    )

    # --------------------------------------------------------
    # CHECKOUT BUTTON
    # --------------------------------------------------------

    if st.button(
        "Proceed to Checkout",
        use_container_width=True,
    ):

        st.session_state.page = "Checkout"

        st.rerun()
