import streamlit as st


def render_home():

    st.markdown(
        """
        <section class="hero">

            <div class="hero-overlay">

                <div class="hero-eyebrow">
                    BENVENUTI A CAFEAI
                </div>

                <h1>
                    La Dolce <span>Pausa.</span>
                </h1>

                <p>
                    Italian-inspired coffee, delicious treats,
                    and your own personal AI barista.
                </p>

            </div>

        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-heading">
            <div class="eyebrow">
                DISCOVER
            </div>

            <h2>
                More than just coffee.
            </h2>

            <p>
                Browse our menu, ask our AI Barista for
                recommendations, and create your perfect order.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ☕
                </div>

                <h3>
                    Artisan Coffee
                </h3>

                <p>
                    Carefully selected coffee drinks
                    inspired by Italian café culture.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🤎
                </div>

                <h3>
                    AI Barista
                </h3>

                <p>
                    Tell CafeAI what you're craving
                    and receive a menu-grounded recommendation.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🥐
                </div>

                <h3>
                    Fresh Treats
                </h3>

                <p>
                    Pair your favorite coffee with
                    something delicious.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="home-quote">

            <div>
                "Coffee is always a good idea."
            </div>

            <span>
                — CafeAI
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )