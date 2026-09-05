import gradio as gr

from app.menu.loader import load_menu
from app.workflows.rag_workflow import build_rag_workflow


# ============================================================
# DATA
# ============================================================

MENU = load_menu()
RAG_APP = build_rag_workflow()


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
# MENU HTML
# ============================================================

def format_price(price: int) -> str:
    return f"NPR {price}"


def create_menu_cards() -> str:

    cards = []

    for item in MENU:

        image = MENU_IMAGES.get(
            item["id"],
            "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"
            "?auto=format&fit=crop&w=900&q=85"
        )

        card = f"""
        <div class="menu-card">

            <img
                class="menu-image"
                src="{image}"
                alt="{item['name']}"
            />

            <div class="menu-card-content">

                <span class="menu-category">
                    {item["category"]}
                </span>

                <h3>
                    {item["name"]}
                </h3>

                <p>
                    {item["description"]}
                </p>

                <div class="menu-price">
                    {format_price(item["price"])}
                </div>

            </div>

        </div>
        """

        cards.append(card)

    return f"""
    <div class="menu-grid">
        {"".join(cards)}
    </div>
    """


# ============================================================
# AI BARISTA
# ============================================================

def ask_barista(message: str, history):

    if not message or not message.strip():

        return (
            "Please ask me something about our menu! ☕"
        )

    try:

        result = RAG_APP.invoke(
            {
                "question": message.strip()
            }
        )

        answer = result.get(
            "answer",
            "I'm sorry, I couldn't find that information."
        )

        sources = result.get("sources", [])

        if sources:

            answer += (
                "\n\n**Menu sources:** "
                + ", ".join(sources)
            )

        return answer

    except Exception as error:

        print(f"CafeAI error: {error}")

        return (
            "Sorry, I ran into a problem. "
            "Please try again."
        )


# ============================================================
# LOAD CSS
# ============================================================

with open(
    "assets/css/style.css",
    "r",
    encoding="utf-8"
) as css_file:

    CUSTOM_CSS = css_file.read()


# ============================================================
# BUILD APP
# ============================================================

with gr.Blocks(
    title="CafeAI — Your AI Barista"
) as demo:

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    gr.HTML(
        """
        <section class="cafe-hero">

            <div class="hero-content">

                <div class="hero-small">
                    Benvenuti a CafeAI
                </div>

                <h1 class="hero-title">
                    La Dolce <span>Pausa.</span>
                </h1>

                <p class="hero-description">
                    Discover beautiful coffee, delicious treats,
                    and your own personal AI barista.
                </p>

            </div>

        </section>
        """
    )


    # ========================================================
    # TABS
    # ========================================================

    with gr.Tabs():


        # ====================================================
        # MENU
        # ====================================================

        with gr.Tab("☕ Menu"):

            gr.Markdown(
                """
                <div class="section-title">
                    Our Menu
                </div>

                <div class="section-subtitle">
                    Italian-inspired coffee, refreshing drinks,
                    tea and freshly baked treats.
                </div>
                """
            )

            gr.HTML(
                create_menu_cards()
            )


        # ====================================================
        # AI BARISTA
        # ====================================================

        with gr.Tab("🤎 AI Barista"):

            gr.HTML(
                """
                <div class="barista-box">

                    <div class="barista-title">
                        Meet your AI Barista
                    </div>

                    <p class="barista-text">
                        Tell me what you're craving and I'll
                        help you discover something from our
                        actual CafeAI menu.
                    </p>

                </div>
                """
            )

            gr.Markdown(
                """
                ### Try asking:

                ☕ *What coffee do you recommend?*

                🍫 *I want something sweet and chocolatey.*

                🧊 *What cold drinks do you have?*

                💪 *What is your strongest coffee?*

                🥐 *What would go well with a latte?*
                """
            )

            chatbot = gr.Chatbot(
                label="CafeAI",
                height=450,
            )

            message = gr.Textbox(
                placeholder="Tell your barista what you're craving...",
                label="Your message",
                lines=2,
            )

            send = gr.Button(
                "Ask my Barista ☕",
                variant="primary",
            )


            def chat(
                message_text,
                history
            ):

                answer = ask_barista(
                    message_text,
                    history
                )

                history = history or []

                history.append(
                    {
                        "role": "user",
                        "content": message_text,
                    }
                )

                history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                return history, ""


            send.click(
                chat,
                inputs=[
                    message,
                    chatbot,
                ],
                outputs=[
                    chatbot,
                    message,
                ],
            )

            message.submit(
                chat,
                inputs=[
                    message,
                    chatbot,
                ],
                outputs=[
                    chatbot,
                    message,
                ],
            )


        # ====================================================
        # ABOUT
        # ====================================================

        with gr.Tab("✨ About"):

            gr.HTML(
                """
                <div class="about-card">

                    <h2>
                        About CafeAI
                    </h2>

                    <p>
                        CafeAI is an AI-powered café assistant
                        built with Python and Generative AI.
                    </p>

                    <h3>
                        Our technology
                    </h3>

                    <p>
                        ☕ Python<br>
                        🤖 Groq GPT-OSS 120B<br>
                        🧠 LangChain<br>
                        🔗 LangGraph<br>
                        🔎 Chroma<br>
                        📚 Retrieval-Augmented Generation<br>
                        🎨 Gradio
                    </p>

                    <h3>
                        Grounded AI
                    </h3>

                    <p>
                        CafeAI retrieves information from the
                        actual café menu before generating an
                        answer. This helps keep recommendations
                        grounded in our menu data.
                    </p>

                </div>
                """
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    demo.launch(
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(),
    )