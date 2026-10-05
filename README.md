# RAG CLI

A lightweight command-line tool for building and querying **Retrieval-Augmented Generation (RAG)** workflows from local files and documents.

RAG CLI allows you to index your own documents, retrieve relevant information using semantic search, and generate answers using an **API-based language model of your choice**.

The goal is to provide a simple way to experiment with RAG workflows without building a full web application.

## Features

* Simple command-line interface
* Ingest documents from local files
* Automatic document chunking
* Generate embeddings for indexed content
* Semantic similarity search
* Retrieve relevant document context
* Generate answers using an external LLM API
* Model selection through configuration
* Configurable embedding model
* Persistent vector storage
* Easy to extend with different models and providers

## How It Works

RAG CLI follows a simple Retrieval-Augmented Generation pipeline:

```text
             Documents
                 │
                 ▼
            Document Ingestion
                 │
                 ▼
               Chunking
                 │
                 ▼
             Embeddings
                 │
                 ▼
            Vector Store
                 │
                 │
User Query ──────┘
     │
     ▼
Semantic Similarity Search
     │
     ▼
Relevant Context
     │
     ▼
      LLM API
     │
     ▼
   Answer
```

Instead of sending the entire document collection to the language model, RAG CLI first retrieves the most relevant chunks and provides them as context to the model.

This helps keep prompts focused on the information that is relevant to the user's question.

## Requirements

* Python 3.14+
* An API key for a supported language model provider
* Internet access for API-based model requests

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd rag-cli
```

Create and activate a virtual environment if needed, then install the project dependencies.

If you are using `uv`:

```bash
uv sync
```

You can then run the CLI with:

```bash
uv run rag-cli --help
```

## Configuration

RAG CLI uses a configuration file to store settings required by the application.

Create your configuration file from the provided example:

```bash
cp conf.toml.example conf.toml
```

On Windows PowerShell:

```powershell
Copy-Item conf.toml.example conf.toml
```

The configuration can contain settings such as:

* API credentials
* Language model selection
* Embedding model
* Vector database/index configuration
* Retrieval parameters
* Generation settings

### Example

```toml
[llm]
model = "your-model-name"
api_key = "your-api-key"

[embedding]
model = "your-embedding-model"
```

> **Important:** `conf.toml` may contain sensitive information and should never be committed to Git. Use `conf.toml.example` as a template instead.

## Usage

Display the available commands:

```bash
uv run rag-cli --help
```

### Ingest Documents

Index documents from a directory:

```bash
uv run rag-cli ingest ./docs
```

The ingestion process reads the documents, splits them into chunks, generates embeddings, and stores the resulting vectors for retrieval.

### Query Your Documents

Once your documents have been indexed, you can query them:

```bash
uv run rag-cli query "What does this project do?"
```

Another example:

```bash
uv run rag-cli query "Summarize the setup instructions"
```

The application retrieves the most relevant document chunks and sends the retrieved context to the configured language model API.

## Language Models

RAG CLI is designed to work with **API-based language models** rather than requiring a model to run locally.

This means the user can choose the model that best fits their requirements, depending on the configured provider and supported API.

For example, different models can be selected depending on priorities such as:

* Response quality
* Speed
* Cost
* Context length
* Model capabilities

The RAG retrieval pipeline remains largely independent from the selected language model.

## Embeddings

Embeddings are used to represent document chunks and user queries as numerical vectors.

When a query is submitted, RAG CLI compares the query embedding against the stored document embeddings and retrieves the most semantically relevant chunks.

This allows the system to find relevant information even when the query does not contain the exact words used in the source documents.

## Project Structure

A simplified project structure looks like this:

```text
rag-cli/
│
├── rag_cli/
│   ├── ...
│   └── ...
│
├── conf.toml.example
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

The project is structured to keep document processing, embedding generation, retrieval, and language model interaction separated so that individual components can be extended or replaced.

## Example Workflow

A typical workflow looks like this:

```bash
# 1. Install the project
uv sync

# 2. Configure the application
# Edit conf.toml with your API and model settings

# 3. Index your documents
uv run rag-cli ingest ./data

# 4. Query your documents
uv run rag-cli query "What are the main topics discussed in these documents?"
```

The system then performs:

```text
Documents
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
    ↓
User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Chunks
    ↓
LLM API
    ↓
Generated Answer
```

## Use Cases

RAG CLI can be useful for:

* Searching personal documentation
* Querying project documentation
* Exploring research papers and technical documents
* Building small knowledge bases
* Experimenting with RAG architectures
* Prototyping AI assistants
* Learning how retrieval-augmented generation works

## Design Goals

The project focuses on keeping the RAG workflow:

* **Simple** — usable directly from the terminal
* **Modular** — individual components can be replaced or extended
* **Model-agnostic** — the generation model is not tied to a local model
* **Lightweight** — no web application is required
* **Practical** — designed for experimenting with real documents and queries

## Future Improvements

Possible future improvements include:

* Support for additional document formats
* Additional vector database backends
* More embedding providers
* Streaming model responses
* Configurable retrieval strategies
* Conversation history
* Reranking retrieved documents
* Improved CLI commands and output formatting

## License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.
