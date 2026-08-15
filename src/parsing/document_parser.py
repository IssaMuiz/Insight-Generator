import pymupdf
from pathlib import Path
from src.parsing.models import Document, Page


def parse_document(file_path: Path) -> Document:
    "Parse a document into a structured Document object"

    document = pymupdf.open(file_path)

    pages = [
        Page(page_number=page_number, text=page.get_text("text"))
        for page_number, page in enumerate(document, start=1)
    ]

    parsed_document = Document(
        filename=file_path.name,
        filepath=file_path,
        page_count=len(document),
        metadata=document.metadata,
        pages=pages,
    )
    document.close()
    return parsed_document
