from src.parsing.models import Page, Document
from src.chunking.models import TextChunk


class TextChunker:
    """Split a cleaned document into a retriever-ready chunks"""

    def __init__(self, chunk_size=300, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: Document) -> list[TextChunk]:
        """
        Chunk an entire cleaned document

        Args:
            document(Document): cleaned document
        Return:
            list: list of chunks dictionaries
        """
        document_chunks = []

        for page in document.pages:
            document_chunks.extend(self.chunk_page(page))
        return document_chunks

    def chunk_page(self, page: Page) -> list[TextChunk]:
        """
        Split a page in a retriever-ready text chunks

        Args:
            page(Page): A single page from a cleaned document

        Return:
            list: list of chunks in a page

        """

        chunks = []

        text = page.text.split()

        if self.chunk_size <= 0 or self.overlap < 0 or self.overlap >= self.chunk_size:
            raise ValueError(
                "Chunk_size and overlap must be greater than zero and overlap must be less the chunk_size"
            )

        step = self.chunk_size - self.overlap

        for start in range(0, len(text), step):
            chunk_text = text[start : start + self.chunk_size]

            chunk_text = " ".join(chunk_text)

            chunks.append(
                TextChunk(
                    chunk_id=f"page_{page.page_number}chunk_{len(chunks)}",
                    text=chunk_text,
                    page_number=page.page_number,
                    chunk_index=len(chunks),
                    word_count=len(chunk_text.split()),
                )
            )

        return chunks
