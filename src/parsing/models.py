from dataclasses import dataclass, field


@dataclass(frozen=True)
class Page:
    """Represent a single page in a document."""

    page_number: int
    text: str


@dataclass(frozen=True)
class Document:
    """Represent a parsed document"""

    filename: str
    filepath: str
    page_count: int
    metadata: dict[str, str | None]
    pages: list[Page] = field(default_factory=list)
