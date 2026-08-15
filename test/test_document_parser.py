import pymupdf
from pathlib import Path
from src.parsing.document_parser import parse_document
from src.parsing.models import Document, Page


def create_test_doc(tmp_path: Path, pages: list[str]) -> Path:
    "Create a temporary pdf for testing"

    doc_path = tmp_path / "test_document.pdf"

    document = pymupdf.open()

    for text in pages:
        page = document.new_page()
        page.insert_text((72, 89), text)

    document.save(doc_path)
    document.close()

    return doc_path


def test_document_parser_returns_document(tmp_path):

    doc_path = create_test_doc(tmp_path, ["Test document"])

    result = parse_document(doc_path)

    assert isinstance(result, Document)


def test_document_parser_returns_correct_filename(tmp_path):

    doc_path = create_test_doc(tmp_path, ["Test document"])

    result = parse_document(doc_path)

    assert result.filename == "test_document.pdf"


def test_document_parser_returns_correct_filepath(tmp_path):
    doc_path = create_test_doc(tmp_path, ["Test document"])

    result = parse_document(doc_path)

    assert result.filepath == doc_path


def test_document_parser_returns_correct_page_count(tmp_path):
    doc_path = create_test_doc(tmp_path, ["page_1", "page_2", "page_3"])

    result = parse_document(doc_path)

    assert result.page_count == 3


def test_document_parser_returns_page_objects(tmp_path):

    doc_path = create_test_doc(tmp_path, ["page_1", "page_2", "page_3"])

    result = parse_document(doc_path)

    assert isinstance(result.pages[0], Page)


def test_document_parser_preserves_page_numbers(tmp_path):

    doc_path = create_test_doc(tmp_path, ["page_1", "page_2", "page_3"])

    result = parse_document(doc_path)

    page_number = [page.page_number for page in result.pages]

    assert page_number == [1, 2, 3]


def test_document_parser_extracts_text(tmp_path):

    doc_path = create_test_doc(tmp_path, ["This is a text"])

    result = parse_document(doc_path)

    assert "This is a text" in result.pages[0].text


def test_document_parser_preserves_empty_pages(tmp_path):

    doc_path = create_test_doc(tmp_path, ["", "This is page 2"])

    result = parse_document(doc_path)

    pages = [page.text for page in result.pages]

    assert len(pages[0]) == 0
    assert len(pages[1]) != 0


def test_document_parser_preserves_metadata(tmp_path):

    doc_path = create_test_doc(tmp_path, ["Metadata test"])

    result = parse_document(doc_path)

    assert isinstance(result.metadata, dict)
