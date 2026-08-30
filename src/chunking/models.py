from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:

    chunk_id: str
    text: str
    page_number: int
    chunk_index: int
    word_count: int
