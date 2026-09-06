import streamlit as st

from app.workflows.rag_workflow import build_rag_workflow


# ============================================================
# LOAD RAG
# ============================================================

@st.cache_resource
def get_rag_app():
    return build_rag_workflow()


# ============================================================
# PAGE
# ============================================================

def render_barista():

    # --------------------------------------------------------
    # AI BARISTA HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="barista-hero">

            <div class="eyebrow">
                IL TUO BARISTA
            </div>

            <h2>
                Meet your AI Barista.
            </h2>

            <p>
                Tell me what you're craving and I'll
                recommend something from our actual menu.
            </p>

        </div>
        """
    )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    prompt = st.chat_input(
        "What are you in the mood for?"
    )

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Your barista is thinking..."
            ):

                try:

                    # Load the RAG application
                    rag_app = get_rag_app()

                    # Send the user's question
                    result = rag_app.invoke(
                        {
                            "question": prompt
                        }
                    )

                    # Get AI answer
                    answer = result.get(
                        "answer",
                        "I couldn't find that information."
                    )

                    # Get sources
                    sources = result.get(
                        "sources",
                        []
                    )

                    # Add sources if available
                    if sources:

                        answer += (
                            "\n\n**Menu sources:** "
                            + ", ".join(sources)
                        )

                except Exception as error:

                    print(
                        f"AI Barista error: {error}"
                    )

                    answer = (
                        "I'm sorry, I couldn't connect "
                        "to the AI Barista right now."
                    )

                # Display answer
                st.markdown(answer)

        # ----------------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
