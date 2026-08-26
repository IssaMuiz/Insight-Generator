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
