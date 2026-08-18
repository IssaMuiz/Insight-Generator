# Document Parsing

## Overview

Document parsing converts a source document into the standard internal representation used by the Insight Generator system.

The parser separates file-format-specific extraction from the rest of the document-processing pipeline. This allows the system to eventually support PDFs, DOCX, HTML, TXT, and other formats without requiring downstream components to understand the original file format.

## Parsing Pipeline

Source Document
↓
Format-specific Parser
↓
Standard Document Representation
↓
Cleaning / Structure Detection / Chunking

## Document Model

The core `Document` model represents an entire source document.

The model contains:

| Field        | Description                               |
| ------------ | ----------------------------------------- |
| `filename`   | Original document filename                |
| `filepath`   | Source document path                      |
| `page_count` | Number of pages represented by the source |
| `metadata`   | Source-document metadata                  |
| `pages`      | Ordered collection of document pages      |

## Page Model

Each page is represented by a `Page` object containing:

| Field         | Description                              |
| ------------- | ---------------------------------------- |
| `page_number` | Position of the page within the document |
| `text`        | Extracted source text                    |
| `spans`       | layout-aware text spans                  |

Page numbers are preserved because source-location information will later support evidence attribution and citations in generated insights.

## Separation of Responsibilities

The parser is responsible for:

- Opening the source document
- Extracting document metadata
- Extracting page-level text
- Preserving page ordering
- Extracting layout-aware text span
- Creating the standard `Document` representation

The parser is not responsible for:

- Text cleaning
- Removing headers or footers
- Chapter detection
- Section detection
- Chunking
- Embedding generation
- Vector storage
- Retrieval
- LLM generation

These responsibilities belong to later stages of the pipeline.

## Testing

The document parser has automated tests covering:

- Creation of the `Document` object
- Filename preservation
- Filepath preservation
- Page-count extraction
- Creation of `Page` objects
- Page-number preservation
- Text extraction
- Empty-page preservation
- Metadata preservation

Tests use temporary documents rather than relying on the project's actual books or documents.

Run the complete test suite with:

`pytest -v`

The parser is considered complete for this stage when the complete test suite passes.

## Design Decision

The project intentionally avoids making the core document representation PDF-specific.

Although PDF is the first supported format, the system is intended to eventually process multiple document types. Format-specific extraction should therefore remain at the ingestion boundary, while downstream components operate on the common `Document` model.

## Current Status

Status: Complete

Implemented:

- [x] Document model
- [x] Page model
- [x] Document parsing
- [x] Metadata extraction
- [x] Page-level text extraction
- [x] Empty-page handling
- [x] Automated tests
- [x] Format-independent internal representation

Next:

- Document text cleaning and normalisation

"""
Updated Document Parser

The document parser was updated to preserve layout-aware text information
during document extraction.

Previously, the parser stored only the raw text extracted from each page.
The updated parser now stores both the page text and individual TextSpan
objects containing structural information extracted from the source PDF.

Each TextSpan preserves:

- Extracted text
- Page number
- Font name
- Font size
- Font flags
- Bounding box coordinates

This additional information is intentionally preserved during parsing rather
than immediately classifying text as a paragraph, heading, chapter, or section.

The parser therefore separates extraction from structural interpretation.

The extraction flow is:

    PDF
      ↓
    PyMuPDF
      ↓
    Document
      ↓
    Page
      ├── text
      └── spans
            ├── text
            ├── font
            ├── font size
            ├── flags
            └── bounding box

This design allows the later structure-analysis stage to use multiple signals,
such as typography, position, spacing, and text patterns, when determining
the structure of non-fiction books.

The parser does not make structural assumptions during extraction. This is
important because Insight Generator is designed to work across different
knowledge-oriented non-fiction books rather than relying on the layout of a
single book.

The parser continues to preserve the original page text so that existing
cleaning and downstream processing remain compatible.

Updated models:

- TextSpan: represents layout-aware extracted text.
- Page: represents a page and its extracted text spans.
- Document: represents the complete parsed document.

This update provides the foundation required for robust book structure
analysis and later source-grounded retrieval.
"""
