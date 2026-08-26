from src.parsing.models import Page, TextSpan
from src.structure.line_grouper import group_spans_into_lines


def test_group_spans_on_same_line():
    spans = [
        TextSpan(
            text="Hello",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(72.0, 100.0, 100.0, 112.0),
        ),
        TextSpan(
            text="world",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(105.0, 100.5, 140.0, 112.5),
        ),
    ]

    page = Page(
        page_number=1,
        text="Hello world",
        spans=spans,
    )

    result = group_spans_into_lines(page)

    assert len(result) == 1
    assert result[0].text == "Hello world"


def test_group_spans_on_different_lines():
    spans = [
        TextSpan(
            text="First line",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(72.0, 100.0, 140.0, 112.0),
        ),
        TextSpan(
            text="Second line",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(72.0, 120.0, 150.0, 132.0),
        ),
    ]

    page = Page(
        page_number=1,
        text="First line\nSecond line",
        spans=spans,
    )

    result = group_spans_into_lines(page)

    assert len(result) == 2
    assert result[0].text == "First line"
    assert result[1].text == "Second line"


def test_grouped_line_preserves_horizontal_reading_order():
    spans = [
        TextSpan(
            text="world",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(120.0, 100.0, 160.0, 112.0),
        ),
        TextSpan(
            text="Hello",
            page_number=1,
            font="LiberationSerif",
            font_size=12.0,
            flags=0,
            bbox=(72.0, 100.0, 110.0, 112.0),
        ),
    ]

    page = Page(
        page_number=1,
        text="Hello world",
        spans=spans,
    )

    result = group_spans_into_lines(page)

    assert result[0].text == "Hello world"


def test_group_spans_returns_empty_for_page_without_spans():
    page = Page(
        page_number=1,
        text="",
        spans=[],
    )

    result = group_spans_into_lines(page)

    assert result == []
