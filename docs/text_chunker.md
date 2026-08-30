# ============================================================

# CHUNKING COMPONENT DOCUMENTATION

# ============================================================

"""
Chunking Component

---

Purpose:
Convert cleaned document pages into smaller, retriever-ready
TextChunk objects.

Why chunking is necessary:
Large documents cannot be passed directly to an embedding model
or LLM efficiently. Chunking divides the document into smaller
pieces so that each piece can later be embedded, stored, and
retrieved independently.

Architecture:

    Cleaned Document
          |
          v
      TextChunker
          |
          +-------------------+
          |                   |
          v                   v
    chunk(document)     chunk_page(page)
          |                   |
          |                   v
          |              Page-level
          |              text chunks
          |                   |
          +--------->---------+
                    |
                    v
          list[TextChunk]

Design Decision:
The public chunk() method operates at the document level, while
chunk_page() performs the actual splitting of individual pages.

    chunk() iterates through every page in the document and uses
    extend() to combine all page-level chunks into a single list.

    Therefore:

        Document -> list[TextChunk]

    This provides a simple document-level interface while keeping
    page-level chunking logic separated and reusable.

Chunking Strategy:
The current implementation uses a word-based sliding window.

    Example:

        chunk_size = 5
        overlap = 2

        Original:
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Chunk 1:
        [1, 2, 3, 4, 5]

        Chunk 2:
        [4, 5, 6, 7, 8]

        Chunk 3:
        [7, 8, 9, 10]

    The movement between chunks is controlled by:

        step = chunk_size - overlap

    Therefore, with:

        chunk_size = 300
        overlap = 50

    the window moves forward by:

        300 - 50 = 250 words

    This creates 50 words of overlap between neighbouring chunks.

Why overlap is used:
Overlap helps preserve contextual information across chunk
boundaries.

    Without overlap, an important idea that happens to cross the
    boundary between two chunks could be separated and become harder
    to retrieve.

    The overlap allows the end of one chunk to appear at the beginning
    of the next chunk.

TextChunk Metadata:
Every generated chunk contains:

        chunk_id
            A unique identifier based on the source page and the
            chunk's position within that page.

            Example:
                page_8chunk_1

        text
            The actual chunk text.

        page_number
            The original page from which the chunk was created.

        chunk_index
            The position of the chunk within its source page.

        word_count
            Number of words contained in the generated chunk.

    Keeping page_number as metadata allows retrieved chunks to be
    traced back to their original location in the document.

Chunk ID Design:
The current implementation uses:

        page_{page_number}chunk_{chunk_index}

    Example:

        page_3chunk_0
        page_3chunk_1
        page_4chunk_0

    The combination of page number and page-local chunk index makes
    the identifier unique across the document.

    A global chunk index is not currently required because chunk_id
    already provides a unique identifier while page_number preserves
    source location.

Validation:
The TextChunker validates its configuration before chunking.

    Required rules:

        chunk_size > 0
        overlap >= 0
        overlap < chunk_size

    Invalid configurations raise ValueError.

    Examples of invalid configurations:

        chunk_size = 0
        chunk_size = -10
        overlap = -5
        overlap >= chunk_size

    This prevents invalid sliding-window behaviour such as a zero or
    negative step.

Empty Text:
Empty pages produce no chunks.

    This prevents the creation of meaningless empty TextChunk objects.

Final Partial Chunk:
If the remaining text is smaller than chunk_size, it is still
returned as the final chunk rather than being discarded.

    This ensures that text at the end of a page is not lost.

Current Architecture:

    PDF
     |
     v
    Parser
     |
     v
    Document / Page
     |
     v
    Cleaner
     |
     v
    TextChunker
     |
     v
    list[TextChunk]
     |
     v
    Embedding

Important Scope Decision:
The current chunker intentionally performs page-level splitting
rather than allowing chunks to cross page boundaries.

    This is a deliberate MVP decision.

    Advantages:
        - Simple implementation
        - Easy to debug
        - Preserves source-page information
        - Easy to inspect retrieved chunks
        - Avoids premature complexity

    Cross-page chunking can be considered later if retrieval evaluation
    demonstrates that page boundaries negatively affect retrieval
    quality.

    The current implementation therefore prioritises simplicity,
    traceability, and maintainability.

Testing:
The chunker is tested using pytest.

    The test suite covers:

    1. Document-level chunking
        Verifies that chunk() processes all pages and returns the
        chunks in a single list.

    2. Page-level chunking
        Verifies that chunk_page() correctly splits a page.

    3. Chunk size
        Verifies that generated chunks follow the configured
        chunk_size.

    4. Overlap
        Verifies that overlapping words are present between adjacent
        chunks.

    5. Final chunk
        Verifies that remaining text is retained.

    6. Empty document
        Verifies that an empty document returns an empty list.

    7. Chunk metadata
        Verifies page_number, chunk_id, chunk_index, and word_count.

    8. Invalid chunk size
        Verifies that chunk_size <= 0 raises ValueError.

    9. Invalid overlap
        Verifies that negative overlap raises ValueError.

    10. Excessive overlap
        Verifies that overlap >= chunk_size raises ValueError.

Testing Philosophy:
The tests focus on observable behaviour rather than implementation
details.

    The goal is to guarantee the contract of TextChunker without making
    the tests dependent on the exact internal implementation.

Current Status:
Chunking implementation: COMPLETE
Chunking validation: COMPLETE
Chunking tests: COMPLETE
Chunking documentation: COMPLETE

Next Component:
Embedding

    The next stage will transform each TextChunk into a numerical
    vector representation that captures its semantic meaning.

    Pipeline:

        TextChunk
            |
            v
        Embedding Model
            |
            v
        Vector
            |
            v
        Vector Store
            |
            v
        Retrieval

"""

# ============================================================
