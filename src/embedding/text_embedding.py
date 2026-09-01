from src.embedding.models import TextEmbed
from src.chunking.models import TextChunk
from sentence_transformers import SentenceTransformer


class TextEmbedding:
    """A class for converting the chunk text into a vector embedding"""

    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        """
        Initialize the embedding generator.

        Args:
            model_name (str): Hugging Face model identifier.
        """
        self.model_name = model_name
        self.model = self.load_model()

    def load_model(self):
        """Load the embedding model
        Returns:
            SentenceTransformer: Loaded embedding model.
        """

        print(f"Load embedding model {self.model_name}")

        model = SentenceTransformer(self.model_name)

        print("Model loaded successfully")

        return model

    def embed(self, chunked_document: list[TextChunk]) -> list[TextEmbed]:
        """
        Embed the document text chunk
        Args:
            chunked_document(list[TextChunk]): a chunked document
        Return:
            list: a vector embedded chunked list
        """

        if not chunked_document:
            return []

        texts = [chunk.text for chunk in chunked_document]

        embedding = self.model.encode(
            texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True
        )

        embedded_chunks = []

        for chunk, embed in zip(chunked_document, embedding):
            embedded_chunks.append(TextEmbed(chunk=chunk, embedding=embed.tolist()))
        return embedded_chunks
