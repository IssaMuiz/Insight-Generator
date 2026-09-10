# Insight Generator

**Insight Generator** is an AI-powered system that analyses practical non-fiction books and transforms their content into a **grounded, structured, and actionable learning guide**.

A user uploads a practical non-fiction book in PDF format, and Insight Generator analyses the book to identify the knowledge that matters most and translate that knowledge into practical actions.

The system is designed to help users answer a more useful question than simply:

> "What does this book say?"

It aims to answer:

> **"What are the most important ideas in this book, why do they matter, and what should I actually do to apply them?"**

The initial system focuses on extracting:

- Core ideas and principles
- Important supporting insights
- Clear explanations of the author's teachings
- Practical lessons
- Concrete, actionable steps
- Supporting passages from the original book

The underlying architecture uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant evidence from the source book before generating the final learning guide.

The first version is **not a document chatbot**. Users do not need to ask questions about the book. The system analyses the uploaded book automatically and produces the structured output.

This repository is also a practical learning project for understanding how modern AI systems are designed, tested, evaluated, deployed, and operated in production.

---

# Project Vision

Practical non-fiction books often contain valuable ideas, frameworks, and methods, but extracting and applying that knowledge can require hours of reading, note-taking, interpretation, and organisation.

A reader may finish a book and still struggle to answer:

- What are the author's most important ideas?
- Which principles are worth remembering?
- What does the author actually want me to change?
- How do these ideas translate into everyday behaviour?
- What specific steps should I take?
- Which parts of the book support these conclusions?

Insight Generator aims to reduce this cognitive burden while preserving the connection between the generated output and the original source.

The long-term vision is to build a system that transforms books into a structured **knowledge-to-action layer**: not merely summarising what an author said, but helping readers understand the author's ideas and translate them into practical behaviour.

---

# Core Product

The first version follows a simple workflow:

```text
Upload Book
     ↓
Analyse Book
     ↓
Identify Core Ideas
     ↓
Retrieve Supporting Evidence
     ↓
Interpret the Ideas
     ↓
Translate Lessons into Actions
     ↓
Generate Structured Learning Guide
```

The final output should help the reader understand:

```text
WHAT
What does the author teach?

WHY
Why does the author believe it matters?

HOW
How can the reader apply it?

EVIDENCE
Which passages from the book support the conclusion?
```

The system should therefore produce something closer to a **practical learning guide** than a conventional summary.

---

# Core Objectives

The project has two primary objectives.

## 1. Build a useful book-to-action system

The system should transform practical non-fiction books into grounded, structured, and actionable knowledge.

The central product objective is:

> **Turn a practical non-fiction book into a useful guide for understanding and applying the author's teachings.**

The generated output should be:

- Grounded in the source
- Focused on the most important ideas
- Understandable
- Practical
- Action-oriented
- Supported by relevant evidence

## 2. Build a production-quality AI engineering project

The project is also an environment for learning and applying:

- Natural Language Processing
- Large Language Models
- Retrieval-Augmented Generation
- Information retrieval
- Embeddings
- Vector search
- Prompt engineering
- Structured generation
- LLM evaluation
- Software engineering
- API development
- Docker
- CI/CD
- Cloud deployment
- Monitoring
- MLOps

---

# Initial Product Scope

The initial MVP is intentionally narrow.

## Input

A practical non-fiction book in PDF format.

Examples include books focused on:

- Habits
- Productivity
- Leadership
- Personal development
- Business
- Psychology
- Finance
- Learning
- Decision-making
- Other practical knowledge domains

## Output

A structured learning guide containing:

### Core Ideas

The most important ideas, principles, frameworks, and teachings in the book.

### Explanations

Clear explanations of what those ideas mean and why they matter.

### Practical Lessons

The useful lessons a reader should take away from the author's arguments and examples.

### Actionable Steps

Concrete actions a reader can take to apply the ideas in real life.

### Supporting Evidence

Relevant passages from the original book that support the generated ideas and recommendations.

---

# What Insight Generator Is Not

The initial version is deliberately **not** intended to be:

- A general-purpose PDF chatbot
- A conversational question-answering system
- A universal document-understanding platform
- A replacement for reading every type of document
- A generic summarisation tool

The system may eventually support these capabilities, but they are not part of the core MVP.

The current focus is:

```text
Book
 ↓
Understanding
 ↓
Core Knowledge
 ↓
Practical Interpretation
 ↓
Action
```

---

# High-Level Architecture

The system follows a retrieval-grounded analysis pipeline:

```text
                  ┌────────────────────────┐
                  │   Practical Book PDF   │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Document Ingestion   │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │        Parsing         │
                  │   Text + Metadata      │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │        Cleaning        │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │        Chunking         │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │       Embeddings        │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │      Vector Store       │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │       Retrieval          │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Evidence Construction │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │      LLM Analysis       │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Structured Learning   │
                  │          Guide          │
                  └────────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │ Core Ideas + Lessons + │
                  │      Action Steps      │
                  └────────────────────────┘
```

The architecture will evolve as the system becomes more sophisticated.

---

# Why RAG?

Large language models are capable of analysing and generating text, but relying entirely on the model's internal knowledge is not sufficient for a system whose output must be grounded in the uploaded book.

Insight Generator therefore uses Retrieval-Augmented Generation as an underlying architectural pattern.

The simplified process is:

```text
Book Content
     ↓
Chunk + Embed
     ↓
Store Vectors
     ↓
Retrieve Relevant Evidence
     ↓
Provide Evidence to LLM
     ↓
Generate Grounded Learning Guide
```

RAG helps the system:

- Ground generated ideas in the original source
- Reduce unsupported claims
- Retrieve relevant evidence from long books
- Preserve a connection between generated insights and source passages
- Work with books that are not part of the model's training knowledge
- Avoid placing the entire book into a single prompt

However, retrieval alone does not produce useful learning material.

The quality of Insight Generator depends on the interaction between:

```text
Retrieval
+
Evidence Selection
+
Reasoning
+
Prompting
+
Structured Generation
+
Evaluation
```

---

# Insight Generation vs Summarisation

Insight Generator is intended to go beyond simply shortening the book.

A conventional summary might produce:

```text
Chapter 1 discusses habits...
Chapter 2 discusses...
Chapter 3 discusses...
```

Insight Generator instead aims for:

```text
Core Idea
    ↓
What the author means
    ↓
Why the idea matters
    ↓
What evidence supports it
    ↓
How to apply it
    ↓
Concrete actions
```

The distinction is important.

The goal is not simply:

> "Tell me what happened in the book."

The goal is:

> **"Help me understand the author's most valuable teachings and put them into practice."**

---

# Planned Capabilities

The capabilities below describe the intended evolution of the system.

## Book Understanding

Analyse the uploaded book and identify useful information such as:

- Pages
- Text
- Metadata
- Structural information
- Relevant passages
- Relationships between sections

Structural information may be used as supporting metadata, but the core pipeline should not depend entirely on successful chapter detection.

## Core Idea Extraction

Identify the major:

- Ideas
- Principles
- Arguments
- Frameworks
- Themes
- Recommendations

The emphasis is on identifying the ideas that provide the greatest value to the reader.

## Insight Generation

Transform important ideas into useful interpretations that explain:

- What the idea means
- Why it matters
- What problem it addresses
- What implications it has
- How it connects to practical behaviour

## Practical Lessons

Translate important ideas into concise lessons that readers can understand, remember, and apply.

## Actionable Steps

Where appropriate, transform lessons into concrete actions.

Examples may include:

- Behaviour changes
- Exercises
- Habits
- Decision processes
- Experiments
- Practical routines
- Implementation steps

The objective is to move from:

```text
Understanding
    ↓
Application
```

rather than stopping at explanation.

## Evidence Linking

Generated ideas and recommendations should be supported by relevant passages from the source book.

This allows the system to preserve a connection between:

```text
Generated Insight
        ↓
Supporting Evidence
        ↓
Original Book
```

## Structured Output

The final result should use a predictable structure so that it can be displayed by a user interface, stored, evaluated, and processed programmatically.

The exact schema will evolve as the generation system develops.

---

# Planned Technology Stack

The exact technologies may change as the project develops. The initial implementation focuses on understanding the underlying components before introducing high-level abstractions.

### Programming

- Python

### Document Processing

- PyMuPDF
- Related document-processing tools where required

### Machine Learning / NLP

- PyTorch
- Sentence Transformers
- Hugging Face ecosystem where appropriate
- Embedding models

### Retrieval

- Vector similarity search
- Vector indexes / vector databases
- Reranking

### LLM

An appropriate LLM provider/model will be selected according to the requirements of each development stage.

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

Technology choices are not treated as fixed requirements. Each technology should justify its role in the system.

---

# Development Philosophy

The system will initially be built **from the fundamentals** rather than immediately depending on frameworks such as LangChain or LlamaIndex.

The purpose is to understand what happens underneath the abstractions.

For each major component, the development process asks:

1. What problem does this component solve?
2. Why is it needed?
3. What alternatives exist?
4. How does it work?
5. How should it be implemented?
6. How should it be tested?
7. How should it be evaluated?
8. How would it work in production?

Higher-level frameworks may be introduced later when their abstractions provide genuine value.

---

# Evaluation

Evaluation is a core part of the project rather than a final-stage addition.

The system must be evaluated at multiple levels.

## Retrieval Evaluation

Potential metrics include:

- Recall@K
- Precision@K
- Mean Reciprocal Rank (MRR)
- NDCG

The objective is to determine whether retrieval returns the evidence necessary for downstream analysis.

## Generation Evaluation

Potential dimensions include:

- Faithfulness
- Relevance
- Completeness
- Coherence
- Groundedness
- Evidence correctness

## Insight Quality

The final output should be evaluated on whether it:

- Captures the important ideas from the source
- Provides useful interpretation
- Remains faithful to the author's teachings
- Avoids unsupported conclusions
- Produces meaningful practical value
- Translates knowledge into useful action
- Provides appropriate supporting evidence

## Actionability

A particularly important evaluation dimension for the MVP is whether the generated action steps are:

- Specific
- Understandable
- Grounded in the book
- Practical
- Relevant to the idea being taught
- Concrete enough for a reader to actually perform

The system should not merely generate motivational statements. The objective is useful action.

---

# Experimentation

Important changes to the system should be measurable.

Examples include:

- Different chunking strategies
- Different chunk sizes
- Different overlap sizes
- Different embedding models
- Different retrieval methods
- Reranking vs no reranking
- Different retrieval query strategies
- Different prompts
- Different LLMs
- Different output schemas
- Different context sizes

Each experiment should ideally answer:

> **Did this change actually improve the quality of the learning guide?**

The project will therefore maintain evaluation results and experiment records as the system evolves.

---

# Production Engineering

After the core intelligence pipeline is working, the project will progressively introduce production engineering practices.

## Testing

Planned testing includes:

- Unit tests
- Integration tests
- Retrieval tests
- Evaluation tests
- Regression tests

## API

Expose the processing pipeline through a production-oriented API.

## Containerisation

Package the application using Docker.

## CI/CD

Automate a workflow similar to:

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

## Versioning

Track important versions of:

- Application code
- Prompts
- Embedding models
- Retrieval configuration
- Evaluation datasets
- Vector indexes
- Model configurations

## Monitoring

Monitor areas such as:

- Processing failures
- Request latency
- Retrieval behaviour
- Token usage
- Generation failures
- Resource utilisation
- System performance

## Cloud Deployment

The final system will be deployed to AWS as part of the project's MLOps learning objectives.

---

# Project Roadmap

The roadmap is divided into progressive stages.

## Phase 1 — Document Understanding

- [x] Define supported document scope
- [x] Collect initial practical non-fiction books
- [x] Analyse source document characteristics
- [x] Build document ingestion foundation
- [x] Implement PDF parsing

## Phase 2 — Text Processing

- [x] Text cleaning
- [x] Normalisation
- [x] Chunking
- [x] Chunk metadata
- [x] Chunking tests

## Phase 3 — Embedding & Retrieval Foundation

- [x] Embedding generation
- [x] Embedding unit tests
- [x] Embedding integration test
- [x] Vector store
- [x] Similarity search
- [ ] Retrieval result model
- [ ] Retrieval evaluation
- [ ] Reranking
- [ ] Retrieval optimisation

## Phase 4 — Analysis Pipeline

- [ ] Internal analysis task design
- [ ] Evidence retrieval strategy
- [ ] Evidence/context construction
- [ ] Prompt construction
- [ ] LLM integration
- [ ] Structured generation
- [ ] Grounded generation
- [ ] Evidence linking

## Phase 5 — Insight Engine

- [ ] Core idea extraction
- [ ] Principle extraction
- [ ] Insight generation
- [ ] Concept explanation
- [ ] Practical lesson generation
- [ ] Actionable step generation
- [ ] Structured learning guide
- [ ] Output validation

## Phase 6 — Evaluation

- [ ] Build evaluation dataset
- [ ] Retrieval evaluation
- [ ] Generation evaluation
- [ ] Faithfulness evaluation
- [ ] Evidence evaluation
- [ ] Insight quality evaluation
- [ ] Actionability evaluation
- [ ] Experiment tracking
- [ ] Regression evaluation

## Phase 7 — Application

- [ ] Build API
- [ ] Build user interface
- [ ] PDF upload
- [ ] Processing pipeline
- [ ] Learning guide display
- [ ] Evidence/source exploration
- [ ] Processing status
- [ ] Error handling

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

These capabilities may be explored after the MVP becomes reliable.

## Interactive Q&A

Allow users to ask follow-up questions about the generated learning guide or source book.

This is intentionally outside the initial product scope.

## Multi-Book Analysis

Compare multiple books and identify:

- Agreements
- Contradictions
- Recurring principles
- Different approaches
- Related concepts

## Knowledge Synthesis

Combine ideas from multiple sources into a unified knowledge model.

## Personal Knowledge Base

Allow users to build a searchable knowledge base from their own collection of books and documents.

## Knowledge-to-Action

Extend the system to generate:

- Personal plans
- Tasks
- Learning objectives
- Practice schedules
- Workflows
- Implementation programmes

These are future directions rather than requirements for the initial MVP.

---

# Project Structure

The repository follows a modular architecture:

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
│   ├── embedding/
│   ├── retrieval/
│   ├── generation/
│   └── evaluation/
│
├── test/
│
├── .gitignore
├── README.md
└── requirements.txt
```

The exact structure will be refined as the architecture develops.

---

# Current Status

**Project Status:** Active Development

The project has completed the foundational document-processing stages:

```text
PDF
 ↓
Parsing ✅
 ↓
Cleaning ✅
 ↓
Chunking ✅
 ↓
Embedding ✅
 ↓
Vector Store ← Current stage
 ↓
Retrieval
 ↓
LLM Analysis
 ↓
Learning Guide
```

The current implementation has established:

- PDF parsing
- Text cleaning
- Page-aware chunking
- Chunk metadata
- Sentence Transformer embeddings
- Unit testing
- Integration testing
- CI validation

The next major objective is to build the vector store and retrieval foundation.

---

# Learning Goals

This project is designed to develop practical understanding of:

- Document AI
- NLP
- LLM applications
- Retrieval-Augmented Generation
- Information retrieval
- Semantic search
- Embeddings
- Vector stores
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

# Success Criteria for the MVP

The MVP should ultimately satisfy the following:

```text
User uploads a practical non-fiction book
                ↓
System processes the book
                ↓
System identifies important ideas
                ↓
System retrieves supporting evidence
                ↓
System generates grounded explanations
                ↓
System converts lessons into practical actions
                ↓
User receives a structured learning guide
```

A successful result should make the reader feel:

> **"I understand what this book is really teaching, why it matters, and what I can actually do with it."**

The system should therefore be judged not only by whether it can process a book, but by whether the resulting output provides enough value to make the effort of using the system worthwhile.

---

# License

License information will be added as the project develops.
