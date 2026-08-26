import re
from src.structure.line_grouper import group_spans_into_lines
from src.parsing.models import Document
from src.structure.models import TextLine, ChapterCandidate, Chapter, CandidateContext


def is_explicit_chapter_heading(text: str) -> bool:
    """Return True when text explicitly identifies itself as a chapter."""

    pattern = r"^\s*chapter\s+(?:\d+|[ivxlcdm]+|one|two|three|four|five|six|seven|eight|nine|ten)\b"

    return bool(re.match(pattern, text, flags=re.IGNORECASE))


def is_numbered_chapter_heading(
    line: TextLine, minimum_font_size: float = 15.0
) -> bool:
    """
    Return True when a line resembles a visually prominent chapter number.
    """

    text = line.text.strip()

    if not text.isdigit():
        return False

    if not line.spans:
        return False

    max_font_size = max(span.font_size for span in line.spans if span is not None)

    return max_font_size >= minimum_font_size


def detect_explicit_chapter_candidates(lines: list[TextLine]) -> list[ChapterCandidate]:
    """Detect lines that explicitly identify themselves as chapters."""

    candidate = []

    for line in lines:
        if not is_explicit_chapter_heading(line.text):
            continue

        candidate.append(
            ChapterCandidate(
                lines=(line,),
                page_number=line.page_number,
                score=1.0,
                reasons=("explicit chapter maker"),
            )
        )

    return candidate


def detect_chapter_candidates(document: Document) -> list[ChapterCandidate]:
    """Detect candidate chapter headings throughout a document."""

    candidate = []

    for page in document.pages:
        page_lines = group_spans_into_lines(page)

        candidate.extend(detect_explicit_chapter_candidates(page_lines))

        candidate.extend(detect_numbered_chapter_candidates(page_lines))

    return candidate


def detect_numbered_chapter_candidates(lines: list[TextLine]) -> list[ChapterCandidate]:
    """Detect visually prominent numbered chapter candidates."""

    candidate = []

    for line in lines:
        if not is_numbered_chapter_heading(line):
            continue

        candidate.append(
            ChapterCandidate(
                lines=(line,),
                page_number=line.page_number,
                score=0.8,
                reasons=(
                    "standalone numeric heading",
                    "visually prominent typography",
                ),
            )
        )
    return candidate


def _looks_like_chapter_title(line: TextLine) -> bool:
    """Return True when a line has basic title-like characteristics."""

    text = line.text.strip()

    if not text:
        return False

    if len(text) > 120:
        return False

    return True


def compose_chapter_heading(
    candidate: ChapterCandidate,
    lines: list[TextLine],
) -> ChapterCandidate:
    """Attach a following title line to a numbered chapter candidate."""

    if len(candidate.lines) != 1:
        return candidate

    candidate_line = candidate.lines[0]

    try:
        index = lines.index(candidate_line)
    except ValueError:
        return candidate

    if index + 1 >= len(lines):
        return candidate

    next_line = lines[index + 1]

    if not _looks_like_chapter_title(next_line):
        return candidate

    return ChapterCandidate(
        lines=(candidate_line, next_line),
        page_number=candidate.page_number,
        score=min(candidate.score + 0.1, 1.0),
        reasons=candidate.reasons + ("followed by title-like line",),
    )


def compose_chapter_headings(
    candidates: list[ChapterCandidate],
    lines: list[TextLine],
) -> list[ChapterCandidate]:
    """Compose titles for all detected chapter candidates."""

    return [compose_chapter_heading(candidate, lines) for candidate in candidates]


def validate_chapter_candidates(
    candidates: list[ChapterCandidate],
    lines: list[TextLine],
) -> list[ChapterCandidate]:
    """Validate chapter candidates using document-level structural evidence."""

    if not candidates:
        return []

    validated_candidates = []

    for candidate in candidates:
        if not candidate.lines:
            continue

        validated_candidates.append(candidate)

    return validated_candidates


def get_chapter_number(
    candidate: ChapterCandidate,
) -> int | None:
    """Return the chapter number represented by a candidate."""

    if not candidate.lines:
        return None

    text = candidate.lines[0].text.strip()

    if text.isdigit():
        return int(text)

    match = re.match(
        r"^chapter\s+(\d+)$",
        text,
        flags=re.IGNORECASE,
    )

    if match:
        return int(match.group(1))

    return None


def group_chapter_sequences(
    candidates: list[ChapterCandidate],
) -> list[list[ChapterCandidate]]:
    """Group chapter candidates into consecutive numbered sequences."""

    if not candidates:
        return []

    numbered_candidates = [
        candidate
        for candidate in candidates
        if get_chapter_number(candidate) is not None
    ]

    if not numbered_candidates:
        return []

    sequences: list[list[ChapterCandidate]] = []
    current_sequence = [numbered_candidates[0]]

    for candidate in numbered_candidates[1:]:
        previous_number = get_chapter_number(current_sequence[-1])
        current_number = get_chapter_number(candidate)

        if (
            previous_number is not None
            and current_number is not None
            and current_number == previous_number + 1
        ):
            current_sequence.append(candidate)
        else:
            sequences.append(current_sequence)
            current_sequence = [candidate]

    sequences.append(current_sequence)

    return sequences


def score_chapter_sequence(
    sequence: list[ChapterCandidate],
) -> float:
    """Score how strongly a candidate sequence resembles a book chapter sequence."""

    if not sequence:
        return 0.0

    score = 0.0

    numbers = [get_chapter_number(candidate) for candidate in sequence]

    numbers = [number for number in numbers if number is not None]

    if not numbers:
        return 0.0

    # Reward longer sequences.
    score += min(len(sequence) / 20, 1.0) * 0.4

    # Reward consecutive numbering.
    if len(numbers) > 1:
        consecutive_pairs = sum(
            current == previous + 1 for previous, current in zip(numbers, numbers[1:])
        )

        continuity = consecutive_pairs / (len(numbers) - 1)
        score += continuity * 0.4

    # Reward sequences beginning with chapter 1.
    if numbers[0] == 1:
        score += 0.2

    return score


def collect_document_lines(document: Document) -> TextLine:
    """Collect document lines in reading order."""

    lines = []
    for page in document.pages:
        lines.extend(group_spans_into_lines(page))

    return lines


def build_chapter(
    lines: list[TextLine], candidates: list[ChapterCandidate]
) -> list[Chapter]:
    """Build chapter structures from ordered chapter candidates."""

    if not candidates:
        return []

    candidates = sorted(
        candidates,
        key=lambda candidate: lines.index(candidate.lines[0]),
    )

    chapters = []

    for index, candidate in enumerate(candidates):

        start_line = candidate.lines[0]

        try:
            start_index = lines.index(start_line)
        except ValueError:
            continue

        if index + 1 < len(candidates):
            next_start_line = candidates[index + 1].lines[0]

            try:
                end_index = lines.index(next_start_line)
            except ValueError:
                continue

        else:
            end_index = len(lines)

        content_start = start_index + len(candidate.lines)

        content = tuple(lines[content_start:end_index])

        chapters.append(Chapter(heading=candidate, content=content))

    return chapters


def build_candidate_context(
    candidate: ChapterCandidate,
    lines: list[TextLine],
    following_count: int = 3,
) -> CandidateContext:
    """Build the local document context surrounding a chapter candidate."""

    if not candidate.lines:
        return CandidateContext(candidate=candidate)

    first_line = candidate.lines[0]
    last_line = candidate.lines[-1]

    try:
        start_index = lines.index(first_line)
        end_index = lines.index(last_line)
    except ValueError:
        return CandidateContext(candidate=candidate)

    previous_line = lines[start_index - 1] if start_index > 0 else None

    next_index = end_index + 1

    next_line = lines[next_index] if next_index < len(lines) else None

    following_lines = tuple(lines[next_index : next_index + following_count])

    return CandidateContext(
        candidate=candidate,
        previous_line=previous_line,
        next_line=next_line,
        following_lines=following_lines,
    )
