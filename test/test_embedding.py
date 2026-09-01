import numpy as np
import src.embedding.text_embedding as embedding_module
from unittest.mock import MagicMock
from src.chunking.models import TextChunk


def test_load_model(monkeypatch, capsys):
    # fake model
    mock_model = MagicMock()

    # Replace SentenceTransformer with a mock function
    def mock_sentence_transformer(model_name):
        return mock_model

    monkeypatch.setattr(
        embedding_module, "SentenceTransformer", mock_sentence_transformer
    )

    # Instatiate text embedding
    embedding = embedding_module.TextEmbedding(model_name="mock_model")

    captured = capsys.readouterr()

    # check our mock model was stored
    assert embedding.model is mock_model

    # check printed output
    assert "Model loaded successfully" in captured.out
    assert f"Load embedding model {embedding.model_name}" in captured.out


def test_embedded_chunks(monkeypatch):
    # fake model
    mock_model = MagicMock()

    mock_model.encode.return_value = [
        np.array([0.1, 0.2, 0.3]),
        np.array([0.4, 0.5, 0.6]),
    ]

    # Replace SentenceTransformer with a mock function
    def mock_sentence_transformer(model_name):
        return mock_model

    monkeypatch.setattr(
        embedding_module, "SentenceTransformer", mock_sentence_transformer
    )

    # Instatiate text embedding
    embedding = embedding_module.TextEmbedding(model_name="mock_model")

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

    result = embedding.embed(chunked_document=chunked_document)

    assert len(result) == 2
    assert result[1].chunk.text == "Another text for text embedding"
    assert result[0].chunk.chunk_id == "page_1chunk_0"
    assert result[0].embedding == [0.1, 0.2, 0.3]
    mock_model.encode.assert_called_once_with(
        [
            "This is a short text",
            "Another text for text embedding",
        ],
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )


def test_embedded_empty_chunks(monkeypatch):
    # fake model
    mock_model = MagicMock()

    # Replace SentenceTransformer with a mock function
    def mock_sentence_transformer(model_name):
        return mock_model

    monkeypatch.setattr(
        embedding_module, "SentenceTransformer", mock_sentence_transformer
    )

    # Instatiate text embedding
    embedding = embedding_module.TextEmbedding(model_name="mock_model")

    chunked_document = []

    result = embedding.embed(chunked_document=chunked_document)

    assert len(result) == 0
    mock_model.encode.assert_not_called()
