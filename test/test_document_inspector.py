import pymupdf
from pathlib import Path
from src.ingestion.document_inspector import inspect_document


def create_test_doc(tmp_doc: Path, pages: list[str]) -> Path:
    "Create a temporary pdf for testing"

    doc_path = tmp_doc / "test_document.pdf"

    document = pymupdf.open()

    for text in pages:
        page = document.new_page()
        page.insert_text((72, 89), text)

    document.save(doc_path)
    document.close()

    return doc_path


def test_inspect_document_returns_correct_filename(tmp_path):
    doc_path = create_test_doc(tmp_path, {"Hello world"})

    results = inspect_document(doc_path)

    assert results["filename"] == "test_document.pdf"


def test_inspect_document_returns_page_count(tmp_path):
    doc_path = create_test_doc(tmp_path, ["page one", "page two", "page three"])

    results = inspect_document(doc_path)

    assert results["page_count"] == 3


def test_inspect_document_returns_extract_page_text(tmp_path):
    doc_path = create_test_doc(tmp_path, ["This is a test document"])

    results = inspect_document(doc_path)

    assert "This is a test document" in results["pages"][0]["text"]


def test_inspect_document_calculates_text_length(tmp_path):
    text = "This is a test."

    doc_path = create_test_doc(
        tmp_path,
        [text],
    )

    result = inspect_document(doc_path)

    assert result["pages"][0]["text_length"] == len(text)


def test_inspect_document_preserves_page_numbers(tmp_path):
    doc_path = create_test_doc(
        tmp_path,
        [
            "First page",
            "Second page",
            "Third page",
        ],
    )

    result = inspect_document(doc_path)

    page_numbers = [page["page_number"] for page in result["pages"]]

    assert page_numbers == [1, 2, 3]


def test_inspect_document_returns_metadata(tmp_path):
    doc_path = create_test_doc(
        tmp_path,
        ["Metadata test"],
    )

    result = inspect_document(doc_path)

    assert isinstance(result["metadata"], dict)


def test_inspect_document_handles_empty_page(tmp_path):
    doc_path = tmp_path / "empty_page.pdf"

    document = pymupdf.open()
    document.new_page()
    document.save(doc_path)
    document.close()

    result = inspect_document(doc_path)

    assert result["page_count"] == 1
    assert result["pages"][0]["text"] == ""
    assert result["pages"][0]["text_length"] == 0
