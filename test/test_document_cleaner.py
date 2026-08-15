from src.cleaning.document_cleaner import clean_text, clean_document
from src.parsing.models import Document, Page


def create_test_document(
    pages: list[str], metadata: dict[str, str | None] | None = None
) -> Document:
    """Create a document object for testing"""

    return Document(
        filename="test_document.pdf",
        filepath="test/test_document.pdf",
        page_count=len(pages),
        metadata=metadata or {},
        pages=[
            Page(page_number=page_number, text=text)
            for page_number, text in enumerate(pages, start=1)
        ],
    )


def test_clean_text_normalises_windows_line_endings():
    text = "First line\r\nSecond line\r\nThird line"

    result = clean_text(text)

    assert result == "First line\nSecond line\nThird line"


def test_clean_text_normalises_old_mac_line_endings():
    text = "First line\rSecond line\rThird line"

    result = clean_text(text)

    assert result == "First line\nSecond line\nThird line"


def test_clean_text_removes_trailing_whitespace():
    text = "First line   \nSecond line\t\nThird line"

    result = clean_text(text)

    assert result == "First line\nSecond line\nThird line"


def test_clean_text_removes_surrounding_whitespace():
    text = "   \n  Some text  \n  "

    result = clean_text(text)

    assert result == "Some text"


def test_clean_text_reduces_excessive_blank_lines():
    text = "Paragraph one.\n\n\n\nParagraph two."

    result = clean_text(text)

    assert result == "Paragraph one.\n\nParagraph two."


def test_clean_text_preserves_internal_line_breaks():
    text = "Chapter One\nIntroduction\nMain idea"

    result = clean_text(text)

    assert result == "Chapter One\nIntroduction\nMain idea"


def test_clean_text_handles_empty_text():
    result = clean_text("")

    assert result == ""


def test_clean_document_returns_document():
    document = create_test_document(["This is a document"])

    result = clean_document(document)

    assert isinstance(result, Document)


def test_clean_document_cleans_page_text():
    document = create_test_document(["Some text\n\n\n\n"])

    result = clean_document(document)

    assert result.pages[0].text == "Some text"


def test_clean_document_preserves_page_numbers():
    document = create_test_document(["page 1", "page 2", "page 3"])

    result = clean_document(document)

    page_numbers = [page.page_number for page in result.pages]

    assert page_numbers == [1, 2, 3]


def test_clean_document_preserves_document_metadata():
    metadata = {"title": "Test Book", "author": "Test Author"}

    document = create_test_document(["Some text"], metadata=metadata)

    result = clean_document(document)

    assert isinstance(result.metadata, dict)
    assert result.metadata == metadata


def test_clean_document_preserves_document_information():

    document = create_test_document(["Some text"])

    result = clean_document(document)

    assert result.filename == "test_document.pdf"
    assert result.filepath == "test/test_document.pdf"
    assert result.page_count == document.page_count


def test_clean_document_does_not_modify_original_document():

    original_text = "Original text  \n\n\n\n\n"

    document = create_test_document([original_text])

    clean_document(document)

    assert document.pages[0].text == original_text


def test_clean_document_handles_empty_pages():

    document = create_test_document(["", "Some text", ""])

    result = clean_document(document)

    assert result.pages[0].text == ""
    assert result.pages[1].text == "Some text"
    assert result.pages[2].text == ""
