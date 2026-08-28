# Vet Vision

Vet Vision is a veterinary and livestock data assistant. It combines:

- SQL queries over livestock disease, incidence, and Maharashtra census data.
- Semantic search over the Standard Veterinary Treatment Guidelines PDF.
- A Gemini tool-calling agent that selects the appropriate source for a question.

## Requirements

- Python 3.13 or newer
- A Gemini API key with available quota
- `uv` (recommended) or the existing `.venv` environment

Set the API key in the shell before running the agent:

```bash
export GEMINI_API_KEY="your-api-key"
```

## Setup

Install the locked dependencies with `uv`:

```bash
uv sync
```

The repository includes the source CSV files, `animal_health.db`, and the treatment-guidelines PDF. To rebuild either generated resource from the source data, run these commands from the project root:

```bash
uv run python convert.py
uv run python rag/ingest.py
```

Run both commands when the database or vector store is missing or the source data has changed. The PDF ingestion step calls Gemini embeddings and therefore also requires `GEMINI_API_KEY`.

## Run

```bash
uv run python main.py
```

The example query in `main.py` asks for national 2015 Foot & Mouth Disease outbreaks and treatment guidance. Edit the `input` value in that file to ask a different question.

The agent uses the following local resources:

- `animal_health.db` for structured statistics and census data.
- `vectorstore/veterinary_guidelines` for treatment-guide retrieval.

## Checks

Run a syntax check without making an API call:

```bash
uv run python -m py_compile main.py db/db.py rag/retriever.py rag/ingest.py convert.py
```

Importing `main.py` does not require credentials. Running the agent or rebuilding the vector store requires a valid `GEMINI_API_KEY` with available quota and network access to Gemini. The application reports quota failures without returning the full API traceback.
