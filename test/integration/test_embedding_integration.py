from src.embedding.text_embedding import TextEmbedding
from src.chunking.models import TextChunk


def test_embedding_chunks_integration():

    chunked_document = [
        TextChunk(
            chunk_id="page_1chunk_0",
            text="This is a short text",
            page_number=1,
            chunk_index=0,
            word_count=5,
        ),
        TextChunk(
            chunk_id="page_1chunk_1",
            text="Another text for text embedding",
            page_number=1,
            chunk_index=1,
            word_count=5,
        ),
    ]

    embedding = TextEmbedding()

    result = embedding.embed(chunked_document=chunked_document)

    assert len(result) == 2
    assert isinstance(result[0].embedding, list)
    assert result[0].chunk.chunk_index == 0
    assert len(result[1].embedding) > 0
