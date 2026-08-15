# Insight Generator

**Insight Generator** is an AI-powered document and book analysis system designed to transform lengthy documents into clear, structured, and actionable insights.

Instead of requiring users to read an entire book or document before understanding its key ideas, Insight Generator analyses the content and helps extract:

- Key ideas and principles
- Important insights
- Chapter summaries
- Practical lessons
- Actionable steps
- Key concepts and explanations
- Supporting passages from the source document

The system uses **Retrieval-Augmented Generation (RAG)** as part of its underlying architecture to ground generated insights in the original document content.

The goal is not simply to build a chatbot that answers questions about a PDF.

The goal is to build an intelligent system that helps users **understand, extract value from, and apply knowledge contained in long-form documents**.

This repository is also a practical learning project for understanding how modern AI systems are designed, evaluated, and deployed in production.

---

## Project Vision

Large documents often contain valuable knowledge, but extracting that knowledge manually can be time-consuming.

A user may have to read hundreds of pages to answer relatively simple questions:

- What are the most important ideas in this book?
- What are the author's main arguments?
- What should I learn from each chapter?
- Which concepts are worth remembering?
- What practical actions can I take?
- Where in the document is this idea supported?

Insight Generator aims to reduce this cognitive and time burden while keeping the generated information grounded in the original source.

The long-term vision is to build a system that can transform large collections of documents into a structured and searchable **knowledge and insight layer**.

---

# Core Objectives

The project has two primary objectives.

### 1. Build a useful document intelligence system

The system should be capable of analysing long-form documents and producing useful, structured outputs.

### 2. Build a production-quality AI engineering project

The project will be developed as a practical environment for learning and applying:

- Natural Language Processing
- Large Language Models
- Retrieval-Augmented Generation
- Information retrieval
- Embeddings
- Vector databases
- Reranking
- Prompt engineering
- LLM evaluation
- Software engineering
- API development
- Docker
- CI/CD
- Cloud deployment
- Monitoring
- MLOps

---

# Planned Capabilities

The initial system is expected to support the following capabilities.

## Document Understanding

Analyse uploaded documents and identify useful structural information such as:

- Document metadata
- Pages
- Chapters
- Sections
- Headings
- Paragraphs
- Text relationships

## Key Idea Extraction

Identify the major ideas, principles, arguments, and themes contained within a document.

## Insight Generation

Go beyond simple summarisation by identifying meaningful implications and insights derived from the source material.

## Chapter Analysis

For each chapter, generate structured information such as:

- Chapter summary
- Main idea
- Important concepts
- Key lessons
- Practical implications
- Supporting passages

## Concept Explanation

Explain important concepts found within the document in a clear and understandable way.

## Practical Lessons

Translate important ideas from the document into lessons that readers can understand and remember.

## Actionable Steps

Where appropriate, transform lessons into concrete actions that a reader can apply.

## Source Evidence

Generated insights should be supported by relevant passages retrieved from the original document.

## Document Question Answering

Users should also be able to ask questions about the uploaded document and receive answers grounded in its contents.

---

# High-Level Architecture

The planned system will follow a pipeline similar to:

```text
                    ┌──────────────────────┐
                    │      Documents       │
                    │  Books / PDFs / etc. │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Document Ingestion │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Parsing        │
                    │  Text + Structure    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Cleaning        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Chunking        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Embeddings + Index   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Retrieval       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Evidence Construction│
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   LLM Generation     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Structured Insights  │
                    └──────────────────────┘
```

The architecture will evolve as the project develops.

---

# Why RAG?

Large language models have strong language understanding and generation capabilities, but they should not be expected to reliably remember or reason over the complete contents of an arbitrary book or document.

RAG allows the system to retrieve relevant information from the original source and provide that information to the language model as context.

The simplified process is:

```text
User Task
    ↓
Retrieve Relevant Evidence
    ↓
Provide Evidence to LLM
    ↓
Generate Grounded Output
```

This helps the system:

- Ground responses in source documents
- Reduce unsupported claims
- Provide source evidence
- Work with documents outside the model's training data
- Handle information that is too large to place directly into a prompt

However, RAG is only one component of Insight Generator.

The project will investigate how **retrieval, reasoning, prompting, structured generation, and evaluation** can work together to produce useful document intelligence.

---

# Insight Generation vs Document Q&A

A major design principle of this project is that **document analysis is broader than question answering**.

A traditional document chatbot might perform:

```text
Question
   ↓
Retrieve chunks
   ↓
LLM
   ↓
Answer
```

Insight Generator aims to support:

```text
Document
   ↓
Understand Structure
   ↓
Identify Important Information
   ↓
Retrieve Supporting Evidence
   ↓
Analyse Information
   ↓
Generate Insights
   ↓
Connect Insights to Evidence
   ↓
Produce Actionable Knowledge
```

This distinction is central to the project's design.

---

# Planned Technology Stack

The exact technologies may change as the project develops, but the initial implementation will focus on understanding the underlying components before introducing high-level frameworks.

### Programming

- Python

### Document Processing

- PyMuPDF and related document-processing tools

### Machine Learning / NLP

- PyTorch
- Hugging Face ecosystem where appropriate
- Embedding models

### Retrieval

- Vector similarity search
- Vector database/index
- Reranking

### LLM

The project will use an LLM provider/model appropriate for the requirements of each development stage.

### Backend

- FastAPI

### Frontend / Prototype

- Streamlit initially

### Containerisation

- Docker

### Version Control

- Git
- GitHub

### Cloud / Deployment

- AWS

### Testing

- pytest

### CI/CD

- GitHub Actions

The technology stack is intentionally not considered final. Technology choices will be evaluated based on requirements rather than added simply because they are popular.

---

# Development Philosophy

The system will initially be built **from the fundamentals** rather than immediately depending on frameworks such as LangChain or LlamaIndex.

The purpose is to understand what happens underneath the abstractions.

For each major component, the development process will ask:

1. What problem does this component solve?
2. Why is it needed?
3. What alternatives exist?
4. How does it work?
5. How should it be implemented?
6. How should it be tested?
7. How should it be evaluated?
8. How would it be implemented in production?

Higher-level frameworks may be introduced later when their abstractions provide genuine value.

---

# Evaluation

Evaluation will be treated as a core part of the system rather than an afterthought.

The project will evaluate both **retrieval quality** and **generation quality**.

## Retrieval Evaluation

Potential metrics include:

- Recall@K
- Precision@K
- Mean Reciprocal Rank (MRR)
- NDCG

The objective is to determine whether the system retrieves the evidence necessary to answer or analyse a task correctly.

## Generation Evaluation

Potential evaluation dimensions include:

- Faithfulness
- Relevance
- Completeness
- Coherence
- Groundedness
- Citation correctness

## Insight Quality

The project will also investigate whether generated insights:

- Capture important ideas from the source
- Provide useful interpretation
- Avoid simply restating the source
- Remain grounded in the document
- Produce practical value

Evaluation methods will evolve as the system becomes more sophisticated.

---

# Experimentation

Important changes to the system should be measurable.

Examples include:

- Different chunking strategies
- Different chunk sizes
- Different embedding models
- Different retrieval methods
- Reranking vs no reranking
- Different prompts
- Different LLMs
- Different context sizes

Each experiment should ideally answer:

> **Did this change actually improve the system?**

The project will therefore maintain evaluation results and experiment records as the system evolves.

---

# Production Engineering

After the core intelligence pipeline is working, the project will progressively introduce production engineering practices.

Planned areas include:

### Testing

- Unit tests
- Integration tests
- Retrieval tests
- Evaluation tests

### API

Expose the core system through a production-oriented API.

### Containerisation

Package the application using Docker.

### CI/CD

Automate:

```text
Code Change
    ↓
Tests
    ↓
Evaluation
    ↓
Build
    ↓
Deployment
```

### Versioning

Track important versions of:

- Application code
- Prompts
- Embedding models
- Retrieval configuration
- Evaluation datasets
- Vector indexes
- Model configurations

### Monitoring

Monitor areas such as:

- Request failures
- Latency
- Retrieval behaviour
- Token usage
- Generation failures
- System performance

### Cloud Deployment

The final system will be deployed to AWS as part of the project's MLOps learning objectives.

---

# Project Roadmap

The roadmap is divided into progressive stages.

## Phase 1 — Document Understanding

- [x] Define supported document types
- [x] Collect initial documents
- [x] Analyse document characteristics
- [x] Build document ingestion pipeline
- [x] Implement PDF parsing

## Phase 2 — Text Processing

- [x] Text cleaning
- [x] Normalisation
- [ ] Chapter detection
- [ ] Section detection
- [ ] Chunking
- [ ] Chunk metadata
- [ ] Evaluate chunking strategies

## Phase 3 — Retrieval System

- [ ] Embedding generation
- [ ] Vector indexing
- [ ] Similarity search
- [ ] Metadata filtering
- [ ] Retrieval evaluation
- [ ] Reranking
- [ ] Retrieval optimisation

## Phase 4 — RAG Pipeline

- [ ] Query processing
- [ ] Context construction
- [ ] Prompt construction
- [ ] LLM integration
- [ ] Grounded generation
- [ ] Source citations
- [ ] Structured outputs

## Phase 5 — Insight Engine

- [ ] Executive summaries
- [ ] Key idea extraction
- [ ] Chapter analysis
- [ ] Concept extraction
- [ ] Concept explanation
- [ ] Practical lessons
- [ ] Actionable steps
- [ ] Evidence linking

## Phase 6 — Evaluation

- [ ] Build evaluation dataset
- [ ] Retrieval evaluation
- [ ] Generation evaluation
- [ ] Faithfulness evaluation
- [ ] Citation evaluation
- [ ] Insight quality evaluation
- [ ] Experiment tracking
- [ ] Regression evaluation

## Phase 7 — Application

- [ ] Build API
- [ ] Build user interface
- [ ] Document upload
- [ ] Processing pipeline
- [ ] Insight dashboard
- [ ] Document Q&A
- [ ] Source exploration

## Phase 8 — Production & MLOps

- [ ] Testing infrastructure
- [ ] Docker
- [ ] CI/CD
- [ ] Configuration management
- [ ] Logging
- [ ] Monitoring
- [ ] Versioning
- [ ] AWS deployment
- [ ] Production evaluation pipeline

---

# Future Possibilities

Once the core system is reliable, the architecture could be extended to support:

### Multi-document analysis

Compare ideas across multiple books, papers, reports, or documents.

### Knowledge synthesis

Identify:

- Agreements
- Contradictions
- Recurring themes
- Different perspectives
- Relationships between concepts

### Personal Knowledge Base

Allow users to build a searchable knowledge base from their own collection of documents.

### Knowledge-to-Action

Transform extracted knowledge into:

- Recommendations
- Plans
- Tasks
- Learning objectives
- Practical workflows

These capabilities are future directions rather than part of the initial MVP.

---

# Project Structure

The initial repository structure will follow a modular architecture:

```text
insight-generator/
│
├── app/
│
├── configs/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
│
├── notebooks/
│
├── scripts/
│
├── src/
│   ├── ingestion/
│   ├── parsing/
│   ├── cleaning/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── generation/
│   └── evaluation/
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

The structure will be refined as the architecture becomes clearer.

---

# Current Status

**Project Status:** Early Development

The project is currently beginning with **document analysis and ingestion**.

The first objective is to understand the characteristics of the source documents before designing the parsing and processing pipeline.

The system will be developed incrementally rather than attempting to implement the complete architecture at once.

---

# Learning Goals

This project is designed to develop practical understanding of:

- Document AI
- NLP
- LLM applications
- RAG
- Information retrieval
- Semantic search
- Embeddings
- Vector databases
- Reranking
- Prompt engineering
- Structured generation
- LLM evaluation
- AI system architecture
- API development
- Docker
- CI/CD
- AWS
- MLOps
- Production AI engineering

The emphasis is on understanding **why systems are designed the way they are**, not merely assembling existing libraries.

---

# License

License information will be added as the project develops.
