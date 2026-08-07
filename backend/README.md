NE RAG Chatbot (backend)

Quick start

1. Create a Python venv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Place your secrets in `.env` (Google API key for Gemini, etc.).

3. Index OKF knowledge YAML files (writes vector DB to `app/database/vector_db`):

```bash
python -c "from app.services.okf_indexer import OKFIndexer; from app.config import KNOWLEDGE_DIR, VECTOR_DB_DIR; OKFIndexer(persist_dir=VECTOR_DB_DIR).index_directory(KNOWLEDGE_DIR)"
```

4. Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints
- `GET /` health
- `POST /index-okf` start indexing (background)
- `POST /query` RAG query (returns answer + hits)

Tests

```bash
pytest -q
```
