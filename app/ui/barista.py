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

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


    if "messages" not in st.session_state:

        st.session_state.messages = []


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    prompt = st.chat_input(
        "What are you in the mood for?"
    )


    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )


        with st.chat_message("user"):

            st.markdown(prompt)


        with st.chat_message("assistant"):

            with st.spinner(
                "Your barista is thinking..."
            ):

                try:

                    rag_app = get_rag_app()

                    result = rag_app.invoke(
                        {
                            "question": prompt
                        }
                    )

                    answer = result.get(
                        "answer",
                        "I couldn't find that information."
                    )

                    sources = result.get(
                        "sources",
                        []
                    )

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


                st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )