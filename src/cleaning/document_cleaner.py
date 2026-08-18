import re
from src.parsing.models import Document, Page


def clean_text(text: str) -> str:
    """Apply safe normalisation to extracted document text."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = "\n".join(line.rstrip() for line in text.split("\n"))

    text = text.strip()

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def clean_document(document: Document) -> Document:
    """Create a cleaned copy of a document"""

    cleaned_pages = [
        Page(page_number=page.page_number, text=clean_text(page.text), spans=page.spans)
        for page in document.pages
    ]

    return Document(
        filename=document.filename,
        filepath=document.filepath,
        page_count=document.page_count,
        metadata=document.metadata.copy(),
        pages=cleaned_pages,
    )
