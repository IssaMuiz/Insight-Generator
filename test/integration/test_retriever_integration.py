from pathlib import Path
from src.retriever.retriever import Retriever
from src.embedding.text_embedding import TextEmbedding
from src.vector_store.vector_store import VectorStore
from src.embedding.models import TextChunk, TextEmbed
from src.vector_store.models import SearchResult


def test_retriever_integration(tmp_path: Path):
    tmp_file = tmp_path / "test_store.pkl"

    text_chunk = [
        TextChunk(
            chunk_id="page_1chunk_0",
            text="First chunk text",
            page_number=1,
            chunk_index=0,
            word_count=len("First chunk text".split()),
        ),
        TextChunk(
            chunk_id="page_1chunk_1",
            text="Second chunk text",
            page_number=1,
            chunk_index=1,
            word_count=len("Second chunk text".split()),
        ),
    ]

    embedding = TextEmbedding()

    text_embed = [
        TextEmbed(
            chunk=text_chunk[0], embedding=embedding.embed_text("First chunk text")
        ),
        TextEmbed(
            chunk=text_chunk[1], embedding=embedding.embed_text("Second chunk text")
        ),
    ]

    vector_store = VectorStore(tmp_file)

    vector_store.add_many(text_embed)
    vector_store.store()
    vector_store.load()

    embedded_query = "Third chunk text"
    retriever = Retriever(vector_store=vector_store, embedding=embedding)

    result = retriever.retrieve(embedded_query, top_k=2)

    assert len(result) == 2
    assert isinstance(result[0], SearchResult)
    assert isinstance(result[1], SearchResult)
    assert result[0].similarity_score >= result[1].similarity_score
