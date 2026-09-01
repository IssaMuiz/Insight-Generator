from dataclasses import dataclass
from src.chunking.models import TextChunk


@dataclass(frozen=True)
class TextEmbed:

    chunk: TextChunk
    embedding: list[float]
