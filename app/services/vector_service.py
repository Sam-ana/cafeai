from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.menu.loader import load_menu


VECTORSTORE_PATH = Path("vectorstore")
COLLECTION_NAME = "cafeai_menu"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def menu_to_documents():
    """Convert menu items into searchable text documents."""

    documents = []

    for item in load_menu():
        text = f"""
Name: {item['name']}
Category: {item['category']}
Price: NPR {item['price']}
Description: {item['description']}
Tags: {', '.join(item.get('tags', []))}
""".strip()

        documents.append(
            {
                "text": text,
                "id": item["id"],
                "category": item["category"],
            }
        )

    return documents


def create_menu_vectorstore():
    """Create the Chroma database from the current menu."""

    embeddings = get_embeddings()
    documents = menu_to_documents()

    texts = [doc["text"] for doc in documents]

    metadatas = [
        {
            "item_id": doc["id"],
            "category": doc["category"],
        }
        for doc in documents
    ]

    ids = [doc["id"] for doc in documents]

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_PATH),
    )

    try:
        vectorstore.delete_collection()
    except Exception:
        pass

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        ids=ids,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTORSTORE_PATH),
    )

    return vectorstore


def get_vectorstore():
    """Load the existing CafeAI menu vector database."""

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(VECTORSTORE_PATH),
    )


def search_menu_knowledge(query: str, k: int = 4):
    """Retrieve the most relevant menu information."""

    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        query,
        k=k,
    )