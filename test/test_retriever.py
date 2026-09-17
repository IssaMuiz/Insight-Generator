from src.retriever.retriever import Retriever
from unittest.mock import MagicMock
from src.vector_store.models import SearchResult
from src.embedding.models import TextEmbed, TextChunk


def test_embed_query():

    mock_embedding = MagicMock()

    embedding = mock_embedding.embed_text.return_value = [1.0, 2.0, 3.0, 4.0]

    mock_vector_store = MagicMock()

    retriever = Retriever(vector_store=mock_vector_store, embedding=mock_embedding)

    result = retriever.embed_query(query="Hello")

    assert result == embedding
    mock_embedding.embed_text.assert_called_once_with("Hello")


def test_retrieve():

    mock_embedding = MagicMock()
    mock_vector = MagicMock()

    embedding = mock_embedding.embed_text.return_value = [1.0, 2.0, 3.0, 4.0]

    mock_vector.search.return_value = [
        SearchResult(
            text_embed=TextEmbed(
                chunk=TextChunk(
                    chunk_id="page1_chunk0",
                    text="Hello World",
                    page_number=1,
                    chunk_index=0,
                    word_count=2,
                ),
                embedding=embedding,
            ),
            similarity_score=0.98,
        )
    ]

    retriever = Retriever(vector_store=mock_vector, embedding=mock_embedding)

    result = retriever.retrieve(query="Hello")

    assert result[0].similarity_score == 0.98
    assert result[0].text_embed.embedding == embedding
    assert result[0].text_embed.chunk.text == "Hello World"
    mock_vector.search.assert_called_once_with(query_embedding=embedding, top_k=5)
