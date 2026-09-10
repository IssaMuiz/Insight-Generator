# Vector Store

## Overview

The Vector Store is responsible for storing embedded book chunks and retrieving the most semantically similar chunks for a given query embedding.

It sits after the embedding stage in the Insight Generator pipeline:

PDF
→ Parsing
→ Cleaning
→ Chunking
→ Embedding
→ Vector Store
→ Retrieval
→ LLM Analysis
→ Structured Learning Guide

The Vector Store is an internal infrastructure component. It is not a user-facing feature.

For the MVP, retrieval is used internally by the analysis pipeline to find relevant passages from the uploaded book.

---

## Purpose

The purpose of the Vector Store is to:

- Store generated text embeddings
- Persist embeddings to disk
- Reload stored embeddings when required
- Compare query embeddings against stored embeddings
- Rank stored records according to similarity
- Return the most relevant source chunks

The Vector Store does not generate embeddings.

Embedding generation is handled by the `TextEmbedding` component.

The separation is:

TextEmbedding
→ creates embeddings

VectorStore
→ stores and searches embeddings

---

## Data Being Stored

The Vector Store stores `TextEmbed` objects.

A `TextEmbed` contains:

TextEmbed
├── chunk
│ └── TextChunk
└── embedding
└── list[float]

The original `TextChunk` is preserved alongside its vector.

This is important because retrieval must eventually return the actual source passage and its metadata, not just a numerical vector.

The stored chunk provides information such as:

- Chunk ID
- Text
- Page number
- Chunk index
- Word count

---

## Search Results

Search results are represented by the `SearchResult` data model.

Conceptually:

SearchResult
├── text_embed
│ └── TextEmbed
└── similarity_score
└── float

The `TextEmbed` contains the source information, while the similarity score represents how closely that stored embedding matches the current query embedding.

The similarity score is query-specific and therefore does not belong inside `TextEmbed`.

---

## Storage

The initial Vector Store uses Python `pickle` for local persistence.

The stored data is written to a `.pkl` file.

Example:

data/
└── processed/
└── vector_store.pkl

The configured file path is supplied when creating the Vector Store.

Conceptually:

VectorStore
├── file_path
└── embedding_records

This allows the storage location to be changed without modifying the storage logic.

---

## `add_many()`

`add_many()` adds multiple `TextEmbed` records to the in-memory vector store.

Input:

`list[TextEmbed]`

Behaviour:

```text
TextEmbed records
      ↓
add_many()
      ↓
embedding_records
```
