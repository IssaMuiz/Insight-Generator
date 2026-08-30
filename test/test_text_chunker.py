import pytest
from src.parsing.models import Page, Document
from src.chunking.text_chunker import TextChunker


def create_test_doc(
    pages: list[str], metadata: dict[str, str | None] | None = None
) -> Document:
    """Create a temporary pdf file"""

    document = Document(
        filename="test_pdf",
        filepath="test/test_pdf",
        page_count=len(pages),
        metadata=metadata or {},
        pages=[
            Page(page_number=page_number, text=text)
            for page_number, text in enumerate(pages, start=1)
        ],
    )

    return document


def test_document_text_chunking():
    test_doc = create_test_doc(
        ["This is a short text for document chunking test", "Another text for testing"],
    )

    chunker = TextChunker(chunk_size=6, overlap=2)

    result = chunker.chunk(test_doc)

    assert result[0].text == "This is a short text for"
    assert result[3].text == "Another text for testing"
    assert result[3].chunk_id == "page_2chunk_0"
    assert result[1].page_number == 1
    assert result[0].chunk_index == 0
    assert result[0].word_count == 6
    assert len(result) == 4


def test_document_empty_page_text_chunking():
    test_doc = create_test_doc([])

    chunker = TextChunker(chunk_size=6, overlap=2)

    result = chunker.chunk(test_doc)

    assert len(result) == 0


def test_page_text_chunking():
    page = Page(
        page_number=1, text="This is a short text for page chunking test", spans=[]
    )

    chunker = TextChunker(chunk_size=5, overlap=1)

    result = chunker.chunk_page(page)

    assert result[0].page_number == 1
    assert result[0].text == "This is a short text"
    assert result[0].chunk_id == "page_1chunk_0"
    assert result[0].word_count == 5


def test_page_text_chunking_overlap():
    page = Page(
        page_number=1, text="This is a short test for page chunking test", spans=[]
    )

    chunker = TextChunker(chunk_size=5, overlap=2)

    result = chunker.chunk_page(page)

    first_chunk = result[0].text.split()
    second_chunk = result[1].text.split()
    assert first_chunk[3:5] == second_chunk[0:2]


def test_invalid_chunk_size():
    page = Page(
        page_number=1, text="This is a short test for page chunking test", spans=[]
    )

    chunker = TextChunker(chunk_size=0, overlap=2)

    with pytest.raises(ValueError):
        chunker.chunk_page(page)


def test_invalid_overlap_size():
    page = Page(
        page_number=1, text="This is a short test for page chunking test", spans=[]
    )

    chunker = TextChunker(chunk_size=5, overlap=-2)

    with pytest.raises(ValueError):
        chunker.chunk_page(page)


def test_overlap_exceed_chunk_size():
    page = Page(
        page_number=1, text="This is a short test for page chunking test", spans=[]
    )

    chunker = TextChunker(chunk_size=5, overlap=7)

    with pytest.raises(ValueError):
        chunker.chunk_page(page)
