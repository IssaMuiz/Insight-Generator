import pymupdf
from pathlib import Path
from src.parsing.models import Document, Page, TextSpan


def parse_document(file_path: Path) -> Document:
    "Parse a document into a structured Document object"

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        spans = extract_text_spans(page, page_number)
        pages.append(Page(page_number=page_number, text=text, spans=spans))

    parsed_document = Document(
        filename=file_path.name,
        filepath=file_path,
        page_count=len(document),
        metadata=document.metadata,
        pages=pages,
    )
    document.close()
    return parsed_document


def extract_text_spans(page, page_number: int) -> list[TextSpan]:
    """Extract text spans and their layout information from a PDF page."""

    spans = []

    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        if "lines" not in block:
            continue

        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]

                if not text.strip():
                    continue

                spans.append(
                    TextSpan(
                        text=text,
                        page_number=page_number,
                        font=span.get("font"),
                        font_size=span.get("size"),
                        flags=span.get("flags"),
                        bbox=tuple(span["bbox"]),
                    )
                )

    return spans
