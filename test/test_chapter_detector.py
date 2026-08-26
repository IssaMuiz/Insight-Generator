from src.parsing.models import Page, TextSpan
from src.structure.models import TextLine, ChapterCandidate
from src.structure.line_grouper import group_spans_into_lines
from src.structure.chapter_detector import (
    detect_explicit_chapter_candidates,
    detect_numbered_chapter_candidates,
    compose_chapter_heading,
    get_chapter_number,
    group_chapter_sequences,
    score_chapter_sequence,
    build_candidate_context,
)


def test_detects_explicit_chapter_heading():

    spans = [
        TextSpan(
            text="Chapter 1",
            page_number=1,
            font="LiberationSerif",
            font_size=24.0,
            flags=20,
            bbox=(100.0, 100.0, 200.0, 125.0),
        )
    ]

    page = Page(page_number=1, text="Chapter 1", spans=spans)

    lines = group_spans_into_lines(page)

    result = detect_explicit_chapter_candidates(lines)

    assert len(result) == 1
    assert result[0].page_number == 1
    assert result[0].lines[0].text == "Chapter 1"
    assert result[0].score == 1.0


def test_does_not_detect_normal_paragraph_as_chapter():
    spans = [
        TextSpan(
            text="This chapter explains the importance of small habits.",
            page_number=1,
            font="LiberationSerif",
            font_size=14.0,
            flags=0,
            bbox=(72.0, 100.0, 500.0, 115.0),
        )
    ]

    page = Page(
        page_number=1,
        text="This chapter explains the importance of small habits.",
        spans=spans,
    )

    lines = group_spans_into_lines(page)

    result = detect_explicit_chapter_candidates(lines)

    assert result == []


def test_chapter_detection_is_case_insensitive():
    spans = [
        TextSpan(
            text="CHAPTER 2",
            page_number=2,
            font="LiberationSerif",
            font_size=24.0,
            flags=20,
            bbox=(100.0, 100.0, 200.0, 125.0),
        )
    ]

    page = Page(
        page_number=2,
        text="CHAPTER 2",
        spans=spans,
    )

    lines = group_spans_into_lines(page)

    result = detect_explicit_chapter_candidates(lines)

    assert len(result) == 1


def test_detect_visually_prominent_numbered_chapter():
    spans = [
        TextSpan(
            text="1",
            page_number=1,
            font="LiberationSerif",
            font_size=23.76,
            flags=4,
            bbox=(300.0, 164.0, 312.0, 188.0),
        )
    ]
    page = Page(page_number=1, text="1", spans=spans)

    lines = group_spans_into_lines(page)

    result = detect_numbered_chapter_candidates(lines)

    assert len(result) == 1
    assert result[0].lines[0].text == "1"
    assert result[0].score == 0.8


def test_does_not_detect_small_numeric_text_as_chapter():
    spans = [
        TextSpan(
            text="365",
            page_number=18,
            font="LiberationSerif",
            font_size=5.76,
            flags=5,
            bbox=(336.33, 241.84, 344.97, 247.60),
        )
    ]

    page = Page(
        page_number=18,
        text="365",
        spans=spans,
    )

    lines = group_spans_into_lines(page)

    result = detect_numbered_chapter_candidates(lines)

    assert result == []


def test_does_not_detect_body_number_as_chapter():
    spans = [
        TextSpan(
            text="149",
            page_number=40,
            font="LiberationSerif",
            font_size=5.76,
            flags=4,
            bbox=(230.72, 282.16, 239.36, 287.92),
        )
    ]

    page = Page(
        page_number=40,
        text="149",
        spans=spans,
    )

    lines = group_spans_into_lines(page)

    result = detect_numbered_chapter_candidates(lines)

    assert result == []


def test_composes_numbered_chapter_with_title():
    number_span = TextSpan(
        text="1",
        page_number=1,
        font="LiberationSerif",
        font_size=23.76,
        flags=4,
        bbox=(300.0, 164.0, 312.0, 188.0),
    )

    title_span = TextSpan(
        text="The Surprising Power of Atomic Habits",
        page_number=1,
        font="LiberationSerif",
        font_size=23.76,
        flags=4,
        bbox=(116.0, 206.5, 495.6, 230.2),
    )

    number_line = TextLine(
        text="1",
        page_number=1,
        spans=[number_span],
    )

    title_line = TextLine(
        text="The Surprising Power of Atomic Habits",
        page_number=1,
        spans=[title_span],
    )

    lines = [
        number_line,
        title_line,
    ]

    candidates = detect_numbered_chapter_candidates(lines)

    assert len(candidates) == 1

    composed = compose_chapter_heading(
        candidates[0],
        lines,
    )

    assert len(composed.lines) == 2
    assert composed.lines[0].text == "1"
    assert composed.lines[1].text == "The Surprising Power of Atomic Habits"


def test_does_not_attach_long_paragraph_as_chapter_title():
    number_span = TextSpan(
        text="1",
        page_number=1,
        font="LiberationSerif",
        font_size=23.76,
        flags=4,
        bbox=(300.0, 164.0, 312.0, 188.0),
    )

    paragraph_span = TextSpan(
        text=(
            "British Cycling changed one day in 2003. "
            "The organization, which was the governing body "
            "for professional cycling in Great Britain, "
            "had recently hired Dave Brailsford as its new "
            "performance director."
        ),
        page_number=1,
        font="LiberationSerif",
        font_size=14.4,
        flags=4,
        bbox=(72.0, 259.0, 540.0, 273.0),
    )

    lines = group_spans_into_lines(
        Page(
            page_number=1,
            text="1\nBritish Cycling changed one day in 2003...",
            spans=[number_span, paragraph_span],
        )
    )

    candidates = detect_numbered_chapter_candidates(lines)

    composed = compose_chapter_heading(
        candidates[0],
        lines,
    )

    assert len(composed.lines) == 1


def test_get_chapter_number_from_numeric_candidate():
    candidate = ChapterCandidate(
        lines=(
            TextLine(
                text="1",
                page_number=16,
                spans=(),
            ),
        ),
        page_number=16,
        score=0.8,
        reasons=("standalone numeric heading",),
    )

    assert get_chapter_number(candidate) == 1


def test_get_chapter_number_from_multi_digit_numeric_candidate():
    candidate = ChapterCandidate(
        lines=(
            TextLine(
                text="20",
                page_number=184,
                spans=(),
            ),
        ),
        page_number=184,
        score=0.8,
        reasons=("standalone numeric heading",),
    )

    assert get_chapter_number(candidate) == 20


def test_get_chapter_number_from_explicit_chapter_candidate():
    candidate = ChapterCandidate(
        lines=(
            TextLine(
                text="CHAPTER 1",
                page_number=209,
                spans=(),
            ),
        ),
        page_number=209,
        score=1.0,
        reasons=("explicit chapter marker",),
    )

    assert get_chapter_number(candidate) == 1


def test_get_chapter_number_from_lowercase_chapter_candidate():
    candidate = ChapterCandidate(
        lines=(
            TextLine(
                text="chapter 20",
                page_number=228,
                spans=(),
            ),
        ),
        page_number=228,
        score=1.0,
        reasons=("explicit chapter marker",),
    )

    assert get_chapter_number(candidate) == 20


def test_get_chapter_number_returns_none_for_non_chapter_candidate():
    candidate = ChapterCandidate(
        lines=(
            TextLine(
                text="References",
                page_number=229,
                spans=(),
            ),
        ),
        page_number=229,
        score=0.5,
        reasons=("text heading",),
    )

    assert get_chapter_number(candidate) is None


def test_get_chapter_number_returns_none_for_empty_candidate():
    candidate = ChapterCandidate(
        lines=(),
        page_number=1,
        score=0.0,
        reasons=(),
    )

    assert get_chapter_number(candidate) is None


def test_groups_consecutive_numeric_chapter_candidates():
    candidates = [
        ChapterCandidate(
            lines=(TextLine(text="1", page_number=10, spans=()),),
            page_number=10,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="2", page_number=20, spans=()),),
            page_number=20,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="3", page_number=30, spans=()),),
            page_number=30,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
    ]

    sequences = group_chapter_sequences(candidates)

    assert len(sequences) == 1
    assert len(sequences[0]) == 3


def test_starts_new_sequence_when_chapter_number_is_not_consecutive():
    candidates = [
        ChapterCandidate(
            lines=(TextLine(text="1", page_number=10, spans=()),),
            page_number=10,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="2", page_number=20, spans=()),),
            page_number=20,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="5", page_number=50, spans=()),),
            page_number=50,
            score=0.8,
            reasons=("standalone numeric heading",),
        ),
    ]

    sequences = group_chapter_sequences(candidates)

    assert len(sequences) == 2
    assert len(sequences[0]) == 2
    assert len(sequences[1]) == 1


def test_groups_explicit_chapter_candidates():
    candidates = [
        ChapterCandidate(
            lines=(TextLine(text="CHAPTER 1", page_number=100, spans=()),),
            page_number=100,
            score=1.0,
            reasons=("explicit chapter marker",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="CHAPTER 2", page_number=101, spans=()),),
            page_number=101,
            score=1.0,
            reasons=("explicit chapter marker",),
        ),
        ChapterCandidate(
            lines=(TextLine(text="CHAPTER 3", page_number=102, spans=()),),
            page_number=102,
            score=1.0,
            reasons=("explicit chapter marker",),
        ),
    ]

    sequences = group_chapter_sequences(candidates)

    assert len(sequences) == 1
    assert len(sequences[0]) == 3


def test_returns_empty_list_when_no_candidates():
    assert group_chapter_sequences([]) == []


def test_ignores_candidates_without_chapter_numbers():
    candidates = [
        ChapterCandidate(
            lines=(TextLine(text="References", page_number=100, spans=()),),
            page_number=100,
            score=0.5,
            reasons=("text heading",),
        )
    ]

    assert group_chapter_sequences(candidates) == []


def test_score_chapter_sequence_returns_zero_for_empty_sequence():
    assert score_chapter_sequence([]) == 0.0


def test_score_chapter_sequence_rewards_consecutive_numbering():
    sequence = [
        ChapterCandidate(
            lines=(
                TextLine(
                    text=str(number),
                    page_number=number,
                    spans=(),
                ),
            ),
            page_number=number,
            score=0.8,
            reasons=("standalone numeric heading",),
        )
        for number in range(1, 21)
    ]

    score = score_chapter_sequence(sequence)

    assert score == 1.0


def test_score_chapter_sequence_penalizes_numbering_gaps():
    sequence = [
        ChapterCandidate(
            lines=(
                TextLine(
                    text=str(number),
                    page_number=number,
                    spans=(),
                ),
            ),
            page_number=number,
            score=0.8,
            reasons=("standalone numeric heading",),
        )
        for number in [1, 2, 4, 5]
    ]

    score = score_chapter_sequence(sequence)

    assert score < 1.0


def test_score_chapter_sequence_rewards_starting_at_one():
    sequence = [
        ChapterCandidate(
            lines=(
                TextLine(
                    text=str(number),
                    page_number=number,
                    spans=(),
                ),
            ),
            page_number=number,
            score=0.8,
            reasons=("standalone numeric heading",),
        )
        for number in [2, 3, 4, 5]
    ]

    score = score_chapter_sequence(sequence)

    assert score < 1.0


def test_build_candidate_context_returns_following_line():

    lines = [
        TextLine(text="1", page_number=1, spans=()),
        TextLine(text="Chapter Title", page_number=1, spans=()),
        TextLine(text="First Paragraph", page_number=1, spans=()),
        TextLine(text="Second Paragraph", page_number=1, spans=()),
    ]

    candidate = ChapterCandidate(
        lines=([lines[0], lines[1]]),
        page_number=1,
        score=0.8,
        reasons=("numeric heading"),
    )

    chapter_context = build_candidate_context(candidate=candidate, lines=lines)

    assert chapter_context.previous_line is None
    assert chapter_context.next_line.text == "First Paragraph"
    assert chapter_context.following_lines == (lines[2], lines[3])


def test_build_candidate_context_returns_previous_line():
    lines = [
        TextLine(text="Previous", page_number=1, spans=()),
        TextLine(text="1", page_number=2, spans=()),
        TextLine(text="Chapter Title", page_number=2, spans=()),
        TextLine(text="Paragraph", page_number=2, spans=()),
    ]

    candidate = ChapterCandidate(
        lines=(lines[1], lines[2]),
        page_number=2,
        score=0.9,
        reasons=("numeric heading",),
    )

    chapter_context = build_candidate_context(candidate=candidate, lines=lines)

    assert chapter_context.previous_line.text == "Previous"
    assert chapter_context.next_line == lines[3]


def test_build_candidate_context_handles_empty_candidate():
    candidate = ChapterCandidate(
        lines=(),
        page_number=1,
        score=0.0,
        reasons=(),
    )

    context = build_candidate_context(candidate, [])

    assert context.candidate == candidate
    assert context.previous_line is None
    assert context.next_line is None
    assert context.following_lines == ()
