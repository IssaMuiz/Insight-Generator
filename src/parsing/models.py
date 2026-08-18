from dataclasses import dataclass, field


@dataclass(frozen=True)
class TextSpan:
    """Represent a piece of text extracted from a document."""

    text: str
    page_number: int
    font: str | None = None
    font_size: float | None = None
    flags: int | None = None
    bbox: tuple[float, float, float, float] | None = None


@dataclass(frozen=True)
class Page:
    """Represent a single page in a document."""

    page_number: int
    text: str
    spans: list[TextSpan] = field(default_factory=list)


@dataclass(frozen=True)
class Document:
    """Represent a parsed document."""

    filename: str
    filepath: str
    page_count: int
    metadata: dict[str, str | None]
    pages: list[Page] = field(default_factory=list)
