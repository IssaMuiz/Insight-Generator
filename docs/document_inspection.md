# Document Ingestion

## Overview

The document ingestion component is the first stage of the Insight Generator pipeline.

Its responsibility is to inspect PDF documents and extract basic structural information that will be used by subsequent document-processing stages.

At this stage, the component does **not** perform:

* Text cleaning
* Chunking
* Embedding generation
* Vector indexing
* Retrieval
* LLM generation

The purpose of this stage is to establish a reliable and testable representation of the raw PDF documents.

---

## Current Pipeline

```text
PDF Document
     ↓
PDF Inspector
     ↓
Structured Inspection Result
```

The current implementation uses **PyMuPDF (`fitz`)** to open and inspect PDF documents.

---

## Responsibilities

The PDF inspector currently extracts:

* Filename
* Filepath
* Page count
* PDF metadata
* Page number
* Page text
* Character count of extracted page text

---

## Structured Output

The `inspect_pdf()` function returns a dictionary with the following structure:

```python
{
    "filename": "...",
    "filepath": "...",
    "page_count": 0,
    "metadata": {
        ...
    },
    "pages": [
        {
            "page_number": 1,
            "text": "...",
            "text_length": 0
        }
    ]
}
```

### Document-level fields

| Field        | Description                     |
| ------------ | ------------------------------- |
| `filename`   | Name of the PDF file            |
| `filepath`   | Path to the PDF                 |
| `page_count` | Number of pages in the document |
| `metadata`   | Metadata provided by the PDF    |

### Page-level fields

| Field         | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| `page_number` | One-based page number                                       |
| `text`        | Raw extracted page text                                     |
| `text_length` | Number of characters after stripping surrounding whitespace |

---

## Why the Inspector Returns Structured Data

The original implementation printed information directly from the inspection function.

This was changed to separate **data processing** from **presentation**.

The inspection function now returns structured data, while `print_inspection()` handles display.

This separation makes the component easier to:

* Test
* Reuse
* Extend
* Integrate into future pipelines
* Log
* Analyse programmatically

The architecture is therefore:

```text
inspect_pdf()
     ↓
Structured data
     ↓
 ┌───┴────────┐
 ↓            ↓
Tests      Presentation
```

---

## Handling Empty Pages

PDF documents may contain pages with no extractable text.

The inspector does not treat this as an error.

Instead, an empty page is represented as:

```python
{
    "page_number": 1,
    "text": "",
    "text_length": 0
}
```

This allows later processing stages to decide how such pages should be handled.

For example, future stages may need to distinguish between:

* genuinely blank pages
* scanned/image-based pages
* pages where text extraction failed
* pages containing only images

---

## Testing

The document ingestion component is covered by automated tests using **pytest**.

The tests verify:

* Correct filename extraction
* Correct page count
* Text extraction
* Text length calculation
* Page-number preservation
* Metadata availability
* Empty-page handling

The tests create temporary PDFs rather than depending on the project's real books.

This keeps the tests:

* Fast
* Reproducible
* Independent of external documents
* Deterministic

### Running the tests

From the project root:

```bash
pytest -v
```

All current tests should pass before this component is considered complete.

---

## Design Principle

The ingestion layer should preserve information rather than aggressively transform it.

At this stage, the system intentionally keeps the extracted page text close to its original representation.

Cleaning, normalisation, structure detection, and chunking will be performed in later stages.

This separation makes it possible to experiment with different processing strategies without repeatedly re-parsing the original documents.

---

## Current Status

**Status: Complete**

The initial PDF inspection component has been implemented and tested successfully.

### Completed

* [x] PDF inspection
* [x] Metadata extraction
* [x] Page extraction
* [x] Page text measurement
* [x] Structured inspection output
* [x] Empty-page handling
* [x] Automated tests

### Next

The next stage will investigate and implement the **document parsing representation** that the rest of the Insight Generator pipeline will consume.
