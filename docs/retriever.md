# Retriever

## Overview

The Retriever is the component responsible for coordinating query embedding and vector similarity search.

It sits between the embedding and vector-store components:

Text Query
→ Retriever
→ Text Embedding
→ Query Embedding
→ Vector Store
→ Ranked Search Results

The Retriever does not generate embeddings itself and does not calculate similarity scores. Its responsibility is to coordinate the components that already provide those capabilities.

For the Insight Generator MVP, retrieval is an internal operation used to obtain relevant passages from an uploaded practical non-fiction book before the content is passed to the analysis and generation stages.

---

## Purpose

The Retriever provides a simple interface for obtaining relevant source passages from the indexed book.

Its main responsibilities are:

- Accept a retrieval query as text
- Convert the query into an embedding
- Pass the query embedding to the Vector Store
- Request the desired number of results
- Return the ranked `SearchResult` objects

The Retriever therefore acts as an orchestration layer between:

- `TextEmbedding`
- `VectorStore`

---

## Position in the Architecture

The current pipeline is:

```text
PDF
 ↓
Parsing
 ↓
Cleaning
 ↓
Chunking
 ↓
Embedding
 ↓
Vector Store
 ↓
Retriever
 ↓
Evidence
 ↓
LLM Analysis
 ↓
Structured Learning Guide
```

The Retriever does not decide what the book's important ideas are.

It simply provides the relevant source material requested by the higher-level analysis pipeline.

---

## Dependencies

The Retriever depends on two components.

### TextEmbedding

Responsible for converting text into numerical vectors.

The Retriever uses:

```text
TextEmbedding.embed_text()
```

to convert a retrieval query into a query embedding.

### VectorStore

Responsible for searching stored document embeddings.

The Retriever uses:

```text
VectorStore.search()
```

to compare the query embedding against stored embeddings and return ranked results.

The Retriever does not need to know how either component internally works.

---

## Data Flow

The complete retrieval operation is:

```text
Internal analysis query
        ↓
Retriever.retrieve()
        ↓
Retriever.embed_query()
        ↓
TextEmbedding.embed_text()
        ↓
Query embedding
        ↓
VectorStore.search()
        ↓
Cosine similarity
        ↓
Ranked SearchResult[]
        ↓
Retriever returns results
```

For example, the analysis pipeline may eventually issue an internal retrieval query such as:

```text
"What are the author's most important principles?"
```

The Retriever passes that text to the embedding component, obtains its vector representation, and sends that vector to the Vector Store.

---

## `embed_query()`

`embed_query()` converts a text query into its numerical embedding.

Input:

```text
str
```

Output:

```text
list[float]
```

The method delegates the actual embedding operation to `TextEmbedding`.

Conceptually:

```text
query text
    ↓
TextEmbedding.embed_text()
    ↓
query embedding
```

The Retriever does not perform any embedding calculations itself.

---

## `retrieve()`

`retrieve()` is the main public operation of the Retriever.

Input:

- `query`
- `top_k`

Output:

- `list[SearchResult]`

The process is:

1. Receive the text query.
2. Convert the query into an embedding using `embed_query()`.
3. Pass the resulting embedding to the Vector Store.
4. Pass `top_k` to the Vector Store.
5. Return the resulting ranked search results.

Conceptually:

```text
retrieve(query, top_k)
        ↓
embed_query(query)
        ↓
query embedding
        ↓
vector_store.search(
    query_embedding,
    top_k
)
        ↓
SearchResult[]
```

---

## `SearchResult`

The Retriever returns the result model produced by the Vector Store.

A `SearchResult` contains:

```text
SearchResult
├── text_embed
│   ├── chunk
│   └── embedding
└── similarity_score
```

The `text_embed` provides the original source chunk and its embedding.

The `similarity_score` describes how similar the source embedding is to the query embedding.

The Retriever does not modify these results.

---

## Separation of Responsibilities

The Retriever intentionally contains very little retrieval logic.

### TextEmbedding

Answers:

> How do I convert text into an embedding?

### VectorStore

Answers:

> Which stored embeddings are most similar to this query embedding?

### Retriever

Answers:

> How do I connect the query text to the vector search?

This separation keeps the system modular.

The architecture is:

```text
TextEmbedding
    ↓
creates embeddings

VectorStore
    ↓
stores and searches embeddings

Retriever
    ↓
coordinates query embedding and vector search
```

---

## Why the Retriever Exists

It would be possible for a higher-level component to call `TextEmbedding` and `VectorStore` directly.

However, that would make the analysis layer responsible for infrastructure details such as:

- Creating query embeddings
- Knowing which embedding component to use
- Calling the Vector Store
- Passing `top_k`
- Coordinating the retrieval process

The Retriever provides a clean abstraction:

```text
Analysis Engine
      ↓
Retriever.retrieve(query)
      ↓
relevant source passages
```

This keeps the higher-level analysis logic focused on analysing the retrieved information rather than managing retrieval infrastructure.

---

## Unit Testing

The Retriever uses mocked dependencies in its unit tests.

The purpose is to test the Retriever independently of the implementations of `TextEmbedding` and `VectorStore`.

The structure is:

```text
                 REAL
              Retriever
              /       \
             /         \
          MOCK         MOCK
     TextEmbedding   VectorStore
```

### Why Mock the Dependencies?

The Retriever is an orchestration component.

Its unit tests should answer questions such as:

- Was the query passed correctly to the embedding component?
- Was the resulting embedding passed correctly to the Vector Store?
- Was `top_k` passed correctly?
- Were the Vector Store results returned unchanged?

The tests should not retest the embedding model or cosine-similarity implementation.

Those behaviours are already tested by their respective components.

---

## `MagicMock` Usage

The unit tests replace the Retriever's dependencies with `MagicMock` objects.

For the embedding dependency:

```text
mock_embedding.embed_text()
```

is configured to return a predictable vector.

For the Vector Store dependency:

```text
mock_vector_store.search()
```

is configured to return predictable `SearchResult` objects.

The tests then verify both outputs and interactions.

For example:

```text
Retriever
    ↓
mock_embedding.embed_text("Hello")
    ↓
[1.0, 2.0, 3.0, 4.0]
    ↓
mock_vector_store.search(
    query_embedding=[1.0, 2.0, 3.0, 4.0],
    top_k=5
)
```

This allows the test to verify that the Retriever correctly connects the two dependencies.

---

## Unit Test Coverage

The Retriever unit tests verify:

### Query Embedding

- Query text is passed to `embed_text()`.
- `embed_text()` is called exactly once.
- The resulting embedding is returned.

### Retrieval

- Query text is passed to the embedding component.
- The generated embedding is passed to the Vector Store.
- `top_k` is passed correctly.
- Search results returned by the Vector Store are returned by the Retriever.
- The retrieved `SearchResult` data remains intact.

---

## Integration Testing

The Retriever also has an integration test using the
