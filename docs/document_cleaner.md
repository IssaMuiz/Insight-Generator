# Document Text Cleaning and Normalisation

## Overview

Document text cleaning is responsible for safely normalising extracted document text before it moves into later processing stages.

The cleaning stage is intentionally conservative. The goal is to improve text consistency without destroying information that may be important for structure detection, retrieval, evidence attribution, or source citations.

## Cleaning Pipeline

Raw Document
↓
Document Parser
↓
Parsed Document
↓
Text Cleaning and Normalisation
↓
Clean Document
↓
Structure Detection / Chunking

## Cleaning Responsibilities

The current cleaning stage performs the following operations:

- Normalises Windows line endings (`\r\n`) to Unix-style line endings (`\n`)
- Normalises old Mac line endings (`\r`) to Unix-style line endings (`\n`)
- Removes trailing whitespace from individual lines
- Removes leading and trailing whitespace from page text
- Reduces excessive consecutive blank lines
- Preserves meaningful internal line breaks
- Preserves empty pages
- Creates a new cleaned `Document` rather than modifying the original document

## Conservative Cleaning Strategy

The cleaner intentionally avoids aggressive transformations.

It does not currently:

- Remove chapter titles
- Remove section headings
- Remove paragraphs
- Remove quotations
- Remove numbers
- Remove lists
- Remove tables
- Remove page information
- Remove citations
- Remove author names
- Delete empty pages
- Combine pages into one large text string

These operations require additional document analysis and should be handled by later stages of the pipeline.

## Empty Pages

Empty pages are preserved during cleaning.

An empty page may represent:

- An intentionally blank page
- An image-only page
- A scanned page where text extraction produced no text
- A page where extraction failed
- A genuine blank page

The cleaning stage therefore cleans the page's text but does not decide whether the page itself should be removed.

For example:

Raw page:

" \n\n "

After cleaning:

""

The `Page` object itself remains in the document.

This preserves the original document structure and page numbering.

## Preservation of the Original Document

The cleaning stage does not modify the original `Document` object.

Instead, it creates a new `Document` containing the cleaned page text.

The transformation is therefore:

Original Document
│
├──────────────→ Remains unchanged
│
↓
Document Cleaner
↓
New Clean Document

This preserves the original extracted representation as a source of truth.

Maintaining the original document will be important later when the system needs to provide supporting passages and source evidence for generated insights.

## Page-Level Cleaning

Cleaning is performed independently for each page.

Document
├── Page 1 → clean
├── Page 2 → clean
├── Page 3 → clean
└── ...

Page numbers, document metadata, filename, filepath, and page count are preserved during this transformation.

## Separation of Responsibilities

The cleaning stage is responsible for text normalisation.

It is not responsible for:

- Chapter detection
- Section detection
- Document structure analysis
- Semantic segmentation
- Chunking
- Embedding generation
- Vector storage
- Retrieval
- LLM generation
- Insight generation

These responsibilities belong to later stages of the Insight Generator pipeline.

## Testing

Automated tests verify:

- Windows line-ending normalisation
- Old Mac line-ending normalisation
- Trailing whitespace removal
- Surrounding whitespace removal
- Excessive blank-line reduction
- Preservation of meaningful blank lines
- Preservation of internal line breaks
- Empty-text handling
- Document creation
- Page-text cleaning
- Page-number preservation
- Metadata preservation
- Document metadata preservation
- Preservation of the original document
- Empty-page handling
- Whitespace-only page handling

The complete test suite should be run with:

pytest -v

The cleaning stage is considered complete when the complete test suite passes.

## Design Decision

The cleaning stage uses a conservative approach because Insight Generator is designed to produce grounded insights from source documents.

Over-aggressive cleaning could remove information needed for:

- Document structure detection
- Retrieval
- Evidence attribution
- Source citations
- Understanding the author's original meaning

Therefore, cleaning focuses on normalisation while leaving structural interpretation to later stages.

## Current Status

Status: Complete

Implemented:

- [x] Line-ending normalisation
- [x] Trailing whitespace removal
- [x] Surrounding whitespace removal
- [x] Excessive blank-line reduction
- [x] Meaningful line-break preservation
- [x] Empty-page preservation
- [x] Metadata preservation
- [x] Original document preservation
- [x] Automated tests
- [x] Documentation

Next:

- Document structure detection
