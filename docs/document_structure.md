DOCUMENTATION: BOOK STRUCTURE DETECTION

The structure detection module is responsible for identifying and constructing chapter-level structure from parsed PDF books. It operates after the document parser and uses the text spans and layout information produced by the parser.

The overall flow is:

PDF
↓
Document Parser
↓
Text Spans
↓
Group Spans Into Lines
↓
Detect Chapter Candidates
↓
Compose Chapter Headings
↓
Validate Candidates
↓
Group Chapter Sequences
↓
Score Sequences
↓
Build Chapters

1. LINE GROUPING

Function:
    group_spans_into_lines(page: Page, y_tolerance: float = 2.0)

Purpose:
    Reconstruct visual text lines from the individual text spans extracted from a PDF.

PDF text extraction does not always return text in the same logical line structure that a human sees on the page. A single visual line may contain multiple spans because of differences in font, formatting, positioning, or other PDF properties.

The function therefore:

    - Returns an empty list when the page contains no spans.
    - Sorts spans according to their position on the page.
    - Groups spans that have sufficiently similar vertical positions.
    - Orders spans inside each line from left to right.
    - Combines their text into a TextLine.
    - Preserves the original TextSpan objects inside the TextLine.

The y_tolerance parameter controls how close two spans must be vertically to belong to the same visual line.

Example:

    TextSpan("The")
    TextSpan("Surprising")
    TextSpan("Power")
    TextSpan("of")
    TextSpan("Atomic")
    TextSpan("Habits")

becomes:

    TextLine("The Surprising Power of Atomic Habits")

This line representation is important because the chapter detector operates on visual lines rather than raw PDF spans.

A critical implementation detail discovered during development was that spans must be sorted primarily by their vertical position before grouping them into lines. Sorting primarily by x-coordinate caused lines to be reconstructed in an incorrect order and prevented the chapter title from being found immediately after the chapter number.

The correct conceptual ordering is:

    1. Sort spans by vertical position.
    2. Group spans that belong to the same visual line.
    3. Sort spans within each visual line from left to right.

2. CHAPTER CANDIDATES

A ChapterCandidate represents text that may be a chapter heading.

A candidate contains information such as:

    - TextLine objects
    - Page number
    - Score
    - Reasons/evidence supporting the candidate

A detected candidate is not automatically considered a real chapter.

The detector intentionally separates detection from validation because text that looks like a chapter can also occur in:

    - tables of contents
    - appendices
    - references
    - indexes
    - ordinary document content

The architecture therefore follows:

    Detection
        ↓
    Candidate
        ↓
    Evidence
        ↓
    Validation
        ↓
    Chapter

3. EXPLICIT CHAPTER DETECTION

The explicit chapter detector identifies headings that contain an explicit chapter marker.

Examples:

    Chapter 1
    Chapter 2
    CHAPTER 1
    CHAPTER 10

These candidates receive strong initial evidence because the text explicitly identifies itself as a chapter.

However, this alone is not sufficient to determine that the candidate represents an actual chapter in the main body of the book.

For example, the appendix of a book may contain:

    CHAPTER 1
    CHAPTER 2
    CHAPTER 3

where these are references to chapters rather than actual chapter boundaries.

Therefore explicit chapter detection must still go through later validation and sequence analysis.

4. NUMBERED CHAPTER DETECTION

During development with Atomic Habits, an important pattern was discovered.

The book does not represent its main chapter headings as:

    CHAPTER 1

Instead, it uses:

    1
    The Surprising Power of Atomic Habits

    2
    ...

Therefore the detector was extended to support standalone numeric chapter headings.

A standalone number is not automatically considered a chapter because books contain many ordinary numbers.

Examples of numbers that may not represent chapters:

    365
    149
    37.78
    2024
    1 percent

The numbered chapter detector therefore considers additional evidence such as:

    - The number is standalone.
    - The typography is visually prominent.
    - The surrounding structure is compatible with a chapter heading.
    - A following line may look like a title.
    - Other candidates form a consistent chapter sequence.

This allows the detector to distinguish a chapter number from ordinary numeric content.

5. CHAPTER TITLE DETECTION

The project contains a lightweight helper:

    _looks_like_chapter_title()

Its purpose is not to perfectly identify titles.

It only provides basic evidence that a line could represent a chapter title.

The current heuristic checks that:

    - The line is not empty.
    - The line is not excessively long.

For example:

    "The Surprising Power of Atomic Habits"

can pass the basic title-like check.

The function intentionally remains simple because different books use different title styles.

It should therefore be considered one signal among several rather than a complete title classifier.

6. COMPOSING NUMBERED CHAPTERS WITH THEIR TITLES

In the Atomic Habits document, the chapter number and chapter title appear on separate visual lines:

    1

    The Surprising Power of Atomic Habits

The numbered chapter detector initially produces:

    ChapterCandidate(
        lines=("1",)
    )

The function:

    compose_chapter_heading()

then examines the following line.

If the following line appears to be a title, it attaches that line to the candidate:

    ChapterCandidate(
        lines=(
            "1",
            "The Surprising Power of Atomic Habits"
        )
    )

This provides a richer chapter representation than keeping only the chapter number.

The function only performs this composition when the candidate currently contains one line. This prevents already-composed candidates from being modified unnecessarily.

7. CANDIDATE CONTEXT

Chapter detection cannot reliably operate using the candidate line alone.

For example:

    1

could be:

    - a chapter number
    - a numbered list item
    - a page number
    - a reference
    - an ordinary number

But:

    1
    The Surprising Power of Atomic Habits
    The Fate of British Cycling changed one day in 2003...

provides significantly stronger evidence that the number represents a chapter.

Therefore the detector uses surrounding document context, including:

    - following lines
    - neighbouring lines
    - page position
    - typography
    - chapter numbering
    - sequence relationships

8. CANDIDATE VALIDATION

Detection intentionally produces possible candidates.

Validation determines which candidates have sufficient evidence to remain part of the chapter structure.

Validation can consider:

    - candidate type
    - chapter number
    - typography
    - following title-like line
    - surrounding context
    - position within the document
    - chapter sequence consistency

The purpose is to avoid making a final structural decision based on a single heuristic.

The design is therefore:

    Detect broadly
        ↓
    Validate using multiple signals
        ↓
    Build reliable structure

9. CHAPTER NUMBER EXTRACTION

The function:

    get_chapter_number()

extracts the numerical chapter identifier from a candidate.

Examples:

    "1"          → 1
    "Chapter 2"  → 2
    "CHAPTER 10" → 10

The extracted number is later used to identify relationships between chapter candidates.

10. CHAPTER SEQUENCE GROUPING

Individual chapter candidates become much more reliable when analysed as a sequence.

For example:

    1
    2
    3
    4
    5
    ...
    20

strongly suggests that the candidates represent actual chapters.

The function:

    group_chapter_sequences()

groups compatible candidates into chapter-number sequences.

During testing with Atomic Habits, two sequences were discovered:

    Sequence 1
    Numbers:
        [1, 2, 3, ..., 20]

    Pages:
        [16, 28, 40, ..., 184]

and:

    Sequence 2
    Numbers:
        [1, 2, 3, ..., 20]

    Pages:
        [209, 210, ..., 228]

This was an important discovery because both sequences were internally consistent, but they did not represent the same structural region of the book.

The first sequence represented the actual chapters.

The second sequence represented chapter references in the appendix.

This demonstrated why sequence detection alone cannot always determine the correct chapter region.

11. SEQUENCE SCORING

The function:

    score_chapter_sequence()

evaluates how strong a chapter sequence is.

A sequence such as:

    1 → 2 → 3 → 4 → 5

provides strong structural evidence.

A sequence such as:

    1 → 4 → 149 → 365

is much weaker.

Sequence scoring therefore provides document-level evidence that complements individual candidate scoring.

However, sequence score alone should not be interpreted as proof that the sequence represents the main chapter structure.

12. BUILDING CHAPTERS

The function:

    build_chapter()

takes validated chapter candidates and uses their positions in the document to determine chapter boundaries.

Conceptually:

    Chapter 1
        ↓
    Chapter 1 content
        ↓
    Chapter 2
        ↓
    Chapter 2 content
        ↓
    Chapter 3
        ↓
    Chapter 3 content

The resulting chapter boundaries can later be used to attach chapter metadata to chunks.

For example:

    {
        "text": "...",
        "page_number": 37,
        "chapter": "The Surprising Power of Atomic Habits"
    }

13. IMPORTANT DISCOVERY: APPENDIX REFERENCES

One of the most important problems discovered while testing Atomic Habits was that the book contains chapter references in the appendix.

The appendix contains:

    CHAPTER 1
    CHAPTER 2
    CHAPTER 3
    ...
    CHAPTER 20

These look exactly like explicit chapter headings from the perspective of a simple detector.

Therefore, explicit chapter detection alone cannot distinguish:

    Actual chapter
from:
    Reference to a chapter

This is a fundamental reason why chapter detection should be treated as a probabilistic structural inference problem rather than a simple text-matching problem.

14. MULTIPLE SIGNALS

The structure detector therefore uses multiple signals.

No single signal is reliable for every book.

A number may be:

    - a chapter number
    - a page number
    - a reference
    - a statistic
    - a list item
    - part of an equation

Similarly, "CHAPTER 1" may be:

    - an actual chapter
    - a table-of-contents entry
    - an appendix reference
    - a reference section entry

Typography may also be ambiguous.

The intended model is:

    Candidate
        +
    Typography
        +
    Context
        +
    Numbering
        +
    Sequence
        +
    Document position
        ↓
    Structural confidence

15. BOOK-TO-BOOK VARIATION

During development, testing against additional books revealed that the initial implementation was too closely adapted to the Atomic Habits layout.

Different books can use completely different structures.

Examples include:

    1
    Chapter Title

    Chapter 1
    Chapter Title

    CHAPTER ONE

    PART I
    Chapter Title

    Chapter Title

Some books may have:

    - numbered chapters
    - unnumbered chapters
    - parts
    - sections
    - complex front matter
    - tables of contents
    - appendices
    - references
    - indexes
    - scanned pages
    - multi-column layouts

Therefore the current structure detector should NOT be considered a universal PDF structure parser.

The project is intentionally focused on practical nonfiction books where the main goal is to extract ideas, principles, lessons, and actionable knowledge.

Structure detection is an optional enrichment layer rather than the core of the entire application.

16. RELATIONSHIP WITH THE RAG PIPELINE

Chapter detection is not required for the core RAG pipeline.

The core pipeline remains:

    PDF
        ↓
    Parsing
        ↓
    Cleaning
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    Vector Store
        ↓
    Retrieval
        ↓
    LLM
        ↓
    Insights

Chapter detection can provide additional metadata:

    Chapter
    Page
    Section
    Source location

This metadata can later improve:

    - retrieval
    - chapter summaries
    - citations
    - navigation
    - organisation of insights
    - actionable lesson generation

If chapter detection fails on a particular book, the document should still be processed by the rest of the pipeline.

17. TESTING

The structure module contains tests for the individual behaviours that have been implemented.

Tests cover areas such as:

    - grouping spans into visual lines
    - handling empty span collections
    - detecting explicit chapter headings
    - detecting numbered chapter headings
    - extracting chapter numbers
    - composing chapter numbers with titles
    - validating candidates
    - grouping chapter sequences
    - scoring chapter sequences
    - building chapters
    - handling invalid or empty input
    - preventing obvious false positives from ordinary numbers

Testing is performed both with synthetic test documents and with the real Atomic Habits document during development.

The purpose of the tests is to guarantee the behaviour of each component, not to claim that the system can perfectly identify chapters in every possible PDF book.

18. CURRENT LIMITATIONS

The current implementation has several known limitations:

    1. PDF layouts vary significantly between books.

    2. Scanned PDFs may contain no extractable text spans and require OCR.

    3. Numbers are inherently ambiguous.

    4. Explicit chapter markers may occur in appendices and references.

    5. Some books use unnumbered chapters.

    6. Complex page layouts can affect span ordering and line reconstruction.

    7. A sequence can be internally valid while still representing references rather than actual chapters.

These limitations are expected and are not reasons to make the entire project significantly more complicated at this stage.

19. DESIGN DECISION

The structure detector is intentionally modular and optional.

The project is not attempting to solve universal document understanding.

The current goal is to build a strong portfolio project around books that require the reader to understand ideas and apply the author's teachings.

Therefore, the architecture prioritises:

    - simple components
    - clear responsibilities
    - testability
    - maintainability
    - useful results on a reasonable set of books
    - graceful failure when structure cannot be confidently detected

Rather than attempting to create a perfect universal chapter detector, the system should provide structural information when sufficient evidence exists and allow the remaining RAG pipeline to continue when it does not.

20. FINAL STRUCTURE

The current structure architecture can be summarised as:

    PDF Parser
        ↓
    TextSpan
        ↓
    group_spans_into_lines()
        ↓
    TextLine
        ↓
    detect chapter candidates
        ↓
    ChapterCandidate
        ↓
    compose_chapter_heading()
        ↓
    validate_chapter_candidates()
        ↓
    get_chapter_number()
        ↓
    group_chapter_sequences()
        ↓
    score_chapter_sequence()
        ↓
    build_chapter()
        ↓
    Chapter-level structure
        ↓
    Chunk metadata
        ↓
    RAG / Insight Generation

The structure detector is therefore one component of the larger Insight Generator system rather than the system itself.