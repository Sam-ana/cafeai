from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY


def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        groq_api_key=GROQ_API_KEY,
    )