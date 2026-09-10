import pytest
from src.vector_store.vector_store import VectorStore
from src.embedding.models import TextEmbed, TextChunk
from pathlib import Path


def test_add_many(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    textchunk = [
        TextChunk(
            chunk_id="page1_chunk0",
            text="first chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("first chunk text".split()),
        ),
        TextChunk(
            chunk_id="page1_chunk1",
            text="second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("second chunk text".split()),
        ),
    ]

    textembedded = [
        TextEmbed(chunk=textchunk[0], embedding=[1.0, 2.0, 3.0, 4.0]),
        TextEmbed(chunk=textchunk[1], embedding=[5.0, 6.0, 7.0, 8.0]),
    ]
    vector_store = VectorStore(path)

    vector_store.add_many(records=textembedded)

    assert len(vector_store.embedding_records) == 2
    assert vector_store.embedding_records[0] == textembedded[0]
    assert vector_store.embedding_records[1] == textembedded[1]


def test_store(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    vector_store = VectorStore(path)

    vector_store.store()

    assert path.exists()


def test_load_store(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    textchunk = [
        TextChunk(
            chunk_id="page1_chunk0",
            text="first chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("first chunk text".split()),
        ),
        TextChunk(
            chunk_id="page1_chunk1",
            text="second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("second chunk text".split()),
        ),
    ]

    textembedded = [
        TextEmbed(chunk=textchunk[0], embedding=[1.0, 2.0, 3.0, 4.0]),
        TextEmbed(chunk=textchunk[1], embedding=[5.0, 6.0, 7.0, 8.0]),
    ]

    vector_store = VectorStore(path)

    vector_store.add_many(textembedded)
    vector_store.store()
    result = vector_store.load()

    assert result == textembedded


def test_load_missing_file(tmp_path):

    path = tmp_path / "empth_file.pkl"

    vector_store = VectorStore(path)

    with pytest.raises(FileNotFoundError):
        vector_store.load()


def test_cosine_similarity(tmp_path: Path):

    path = tmp_path / "test_store.pkl"

    vector_store = VectorStore(path)

    assert vector_store.cosine_similarity([1, 0], [1, 0]) == 1
    assert vector_store.cosine_similarity([1, 0], [0, 1]) == 0
    assert vector_store.cosine_similarity([1, 0], [-1, 0]) == -1


def test_search(tmp_path: Path):

    path = tmp_path / "test_store.pkl"

    textchunk = [
        TextChunk(
            chunk_id="page1_chunk0",
            text="first chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("first chunk text".split()),
        ),
        TextChunk(
            chunk_id="page1_chunk1",
            text="second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("second chunk text".split()),
        ),
    ]

    textembedded = [
        TextEmbed(chunk=textchunk[0], embedding=[1.0, 2.0, 3.0, 4.0]),
        TextEmbed(chunk=textchunk[1], embedding=[5.0, 6.0, 7.0, 8.0]),
    ]

    vector_store = VectorStore(path)

    vector_store.add_many(textembedded)
    vector_store.store()
    vector_store.load()
    result = vector_store.search([1.0, 2.0, 3.0, 4.0])

    assert result[0].similarity_score == 1
    assert result[0].similarity_score > result[1].similarity_score
    assert result[1].text_embed.chunk.text == "second chunk text"


def test_search_top_k(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    textchunk = [
        TextChunk(
            chunk_id="page1_chunk0",
            text="first chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("first chunk text".split()),
        ),
        TextChunk(
            chunk_id="page1_chunk1",
            text="second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("second chunk text".split()),
        ),
        TextChunk(
            chunk_id="page2_chunk0",
            text="third chunk text",
            page_number=2,
            chunk_index=0,
            word_count=len("third chunk text".split()),
        ),
    ]

    textembedded = [
        TextEmbed(chunk=textchunk[0], embedding=[1.0, 2.0, 3.0, 4.0]),
        TextEmbed(chunk=textchunk[1], embedding=[5.0, 6.0, 7.0, 8.0]),
        TextEmbed(chunk=textchunk[2], embedding=[9.0, 10.0, 11.0, 12.0]),
    ]

    vector_store = VectorStore(path)

    vector_store.add_many(textembedded)
    vector_store.store()
    vector_store.load()
    result = vector_store.search(query_embedding=[1.0, 2.0, 3.0, 4.0], top_k=2)

    assert len(result) == 2


def test_search_invalid_top_k(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    textchunk = [
        TextChunk(
            chunk_id="page1_chunk0",
            text="first chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("first chunk text".split()),
        ),
        TextChunk(
            chunk_id="page1_chunk1",
            text="second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("second chunk text".split()),
        ),
    ]

    textembedded = [
        TextEmbed(chunk=textchunk[0], embedding=[1.0, 2.0, 3.0, 4.0]),
        TextEmbed(chunk=textchunk[1], embedding=[5.0, 6.0, 7.0, 8.0]),
    ]

    vector_store = VectorStore(path)

    vector_store.add_many(textembedded)
    vector_store.store()
    vector_store.load()

    with pytest.raises(ValueError):
        vector_store.search([1.0, 2.0, 3.0, 4.0], top_k=-1)

    with pytest.raises(ValueError):
        vector_store.search([1.0, 2.0, 3.0, 4.0], top_k=0)


def test_search_empty_store(tmp_path: Path):
    path = tmp_path / "test_store.pkl"

    vector_store = VectorStore(path)

    result = vector_store.search(query_embedding=[1.0, 2.0, 3.0, 4.0])

    assert result == []
