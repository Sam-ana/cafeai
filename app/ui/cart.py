import streamlit as st


def calculate_total():

    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


def render_cart():

    st.markdown(
        """
        <div class="section-heading">

            <div class="eyebrow">
                IL TUO ORDINE
            </div>

            <h2>
                Your Cart
            </h2>

        </div>
        """,
        unsafe_allow_html=True,
    )


    cart = st.session_state.cart


    if not cart:

        st.info(
            "Your cart is empty. "
            "Visit the Menu to add something delicious. ☕"
        )

        return


    for index, item in enumerate(cart):

        col1, col2, col3, col4 = st.columns(
            [4, 1, 1, 1]
        )


        with col1:

            st.markdown(
                f"""
                **{item["name"]}**

                NPR {item["price"]} each
                """
            )


        with col2:

            st.write(
                f"Qty: {item['quantity']}"
            )


        with col3:

            subtotal = (
                item["price"]
                * item["quantity"]
            )

            st.write(
                f"NPR {subtotal}"
            )


        with col4:

            if st.button(
                "Remove",
                key=f"remove_{index}",
            ):

                st.session_state.cart.pop(
                    index
                )

                st.rerun()


    st.divider()


    total = calculate_total()


    st.markdown(
        f"""
        <div class="cart-total">

            <span>
                Total
            </span>

            <strong>
                NPR {total}
            </strong>

        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "Proceed to Checkout",
        use_container_width=True,
    ):

        st.session_state.page = "Checkout"

        st.rerun()