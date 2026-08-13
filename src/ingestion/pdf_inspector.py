import pymupdf

from pathlib import Path

RAW_DATA_DIR = Path("../data/raw")


def inspect_pdf(pdf_path: Path) -> None:
    """Inspect a PDF and return basic document information."""

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        text_length = len(text.strip())

        pages.append(
            {"page_number": page_number, "text": text, "text_length": text_length}
        )

    results = {
        "filename": pdf_path.name,
        "filepath": str(pdf_path),
        "page_count": len(document),
        "metadata": document.metadata,
        "pages": pages,
    }

    document.close()
    return results
