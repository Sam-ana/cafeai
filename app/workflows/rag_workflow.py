from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.services.vector_service import search_menu_knowledge
from app.services.groq_service import get_llm


class RAGState(TypedDict, total=False):
    question: str
    context: str
    answer: str
    sources: list[str]


def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant menu information."""

    results = search_menu_knowledge(
        state["question"],
        k=4,
    )

    context_parts = []
    sources = []

    for result in results:
        context_parts.append(result.page_content)

        item_id = result.metadata.get("item_id")

        if item_id:
            sources.append(item_id)

    return {
        **state,
        "context": "\n\n".join(context_parts),
        "sources": list(dict.fromkeys(sources)),
    }


def generate_answer(state: RAGState) -> RAGState:
    """Generate a grounded answer using the retrieved context."""

    llm = get_llm()

    prompt = f"""
You are CafeAI, a friendly AI barista.

Answer the customer's question using ONLY the menu information
provided below.

If the answer cannot be found in the menu information, say:

"I don't have that information in the CafeAI menu."

Do not invent:
- products
- prices
- ingredients
- availability
- sizes

MENU INFORMATION:
{state.get("context", "")}

CUSTOMER QUESTION:
{state["question"]}

Give a concise, friendly answer.
"""

    response = llm.invoke(prompt)

    answer = response.content

    return {
        **state,
        "answer": answer,
    }


def build_rag_workflow():
    """Build and compile the CafeAI RAG workflow."""

    workflow = StateGraph(RAGState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate_answer", generate_answer)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "generate_answer")
    workflow.add_edge("generate_answer", END)

    return workflow.compile()