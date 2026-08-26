from dataclasses import dataclass
from enum import Enum
from src.parsing.models import TextSpan


class BlockType(str, Enum):
    """Types of structural blocks in a non-fiction book."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CHAPTER = "chapter"
    SECTION = "section"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TextLine:
    """Represent a visual line composed of one or more text spans."""

    text: str
    page_number: int
    spans: tuple[TextSpan, ...]


@dataclass(frozen=True)
class StructuralBlock:
    """Represent a structurally classified piece of book content."""

    text: str
    block_type: BlockType
    page_number: int


@dataclass(frozen=True)
class ChapterCandidate:
    """Represent a possible chapter heading detected from book content"""

    lines: tuple[TextLine, ...]
    page_number: int
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class CandidateContext:
    """Represent the local document context surrounding a chapter candidate."""

    candidate: ChapterCandidate
    previous_line: TextLine | None = None
    next_line: TextLine | None = None
    following_lines: tuple[TextLine, ...] = ()


@dataclass(frozen=True)
class Chapter:
    """Represent a detected chapter and its content."""

    heading: ChapterCandidate
    content: tuple[TextLine, ...]
