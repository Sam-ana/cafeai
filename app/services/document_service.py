from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def split_text(text: str):
    """Split document text into smaller chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    return splitter.split_text(text)


def process_pdf(file_path: str):
    """Extract and split a PDF into chunks."""

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise ValueError(
            "No readable text was found in this PDF."
        )

    chunks = split_text(text)

    return chunks