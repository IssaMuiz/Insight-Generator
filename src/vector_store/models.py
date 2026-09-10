from dataclasses import dataclass
from src.embedding.models import TextEmbed


@dataclass(frozen=True)
class SearchResult:

    text_embed: TextEmbed
    similarity_score: float
