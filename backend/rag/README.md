# rag

## Purpose
Layer 5: Retrieval-Augmented Generation. Embeds evidence, stores it in a vector index, retrieves the most relevant chunks for a question, and produces a grounded, cited answer via Groq.

## Files
- `embeddings.py` — loads the `all-MiniLM-L6-v2` sentence-transformer model and exposes `create_embeddings` (384-dim vectors).
- `vector_store.py` — `EvidenceVectorStore`; tries Qdrant first, falls back to in-memory FAISS `IndexFlatL2` if Qdrant is unavailable. Supports `add` and `search`.
- `retriever.py` — `EvidenceRetriever`; embeds the question, searches the store, and reranks results by word-overlap with the question.
- `prompt_builder.py` — builds the LLM prompt with strict JSON output instructions, treating evidence as untrusted data.
- `rag_service.py` — `RAGService.answer` orchestrates retrieve → sanitize → LLM call → parse → validate, with a deterministic mock fallback if Groq is not configured. Citations carry `source` (filename) + `page`.
- `response_validator.py` — `validate_response` returns `{valid, warnings}` based on whether supporting evidence was found.
- `__init__.py` — wires the shared `embed_model` and `vector_store` singletons used across the app.

## How it fits into the pipeline
Evidence from `document_processing/` is indexed here by `decision_service.py`. `api/copilot.py` exposes it as the Copilot chat endpoint.
