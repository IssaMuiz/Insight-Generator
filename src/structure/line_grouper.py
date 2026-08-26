from src.parsing.models import Page
from src.structure.models import TextLine, TextSpan


def group_spans_into_lines(
    page: Page,
    y_tolerance: float = 2.0,
) -> list[TextLine]:
    """Group text spans that belong to the same visual line."""

    if not page.spans:
        return []

    sorted_spans = sorted(
        page.spans,
        key=lambda span: (span.bbox[1], span.bbox[0]),
    )

    lines: list[list[TextSpan]] = []

    for span in sorted_spans:
        if not lines:
            lines.append([span])
            continue

        current_line = lines[-1]
        reference_span = current_line[0]

        if abs(span.bbox[1] - reference_span.bbox[1]) <= y_tolerance:
            current_line.append(span)
        else:
            lines.append([span])

    text_lines = []

    for line_spans in lines:
        ordered_spans = sorted(
            line_spans,
            key=lambda span: span.bbox[0],
        )

        text = " ".join(
            span.text.strip() for span in ordered_spans if span.text.strip()
        )

        if not text:
            continue

        text_lines.append(
            TextLine(
                text=text,
                page_number=page.page_number,
                spans=tuple(ordered_spans),
            )
        )

    return text_lines
