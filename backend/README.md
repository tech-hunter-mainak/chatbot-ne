# NE Backend

FastAPI + FAISS + sentence-transformers + a local Ollama LLM.

One FAISS index per language, built from plain `.txt` files in `knowledge/<lang>/`.

## Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # paths, model names, supported languages
│   ├── api/chat.py              # POST /chat
│   ├── models/schemas.py        # request/response models
│   ├── services/
│   │   ├── embedding_service.py # sentence-transformers wrapper
│   │   ├── retrieval_service.py # chunking + top-k retrieval
│   │   ├── llm_service.py       # calls local Ollama server 
│   │   └── rag_service.py       # ties retrieval + generation together
│   └── vectorstore/faiss_manager.py  # per-language FAISS index (build/load/search)
├── knowledge/<lang>/*.txt       # source text per language (asm, kha, grt, lus)
├── scripts/build_index.py       # builds/rebuilds FAISS indexes from knowledge/
├── database/vector_db/          # generated index + metadata files (gitignored)
└── requirements.txt
```

## Setup

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# install Ollama : https://ollama.com/download
ollama pull llama3.2   
ollama serve               # localhost:11434
```

Any Ollama-supported model works — just set `LLM_MODEL` in `.env` to match
whatever you `ollama pull`. Smaller models (`llama3.2:1b`, `qwen2.5:0.5b`) run
fine on modest hardware/CPU if you don't have a GPU.

## Add knowledge

Drop `.txt` files into `knowledge/<lang_code>/`. Supported codes are defined
in `app/config.py` (`SUPPORTED_LANGUAGES`) — currently `asm`, `kha`, `grt`, `lus`.
Add a new folder + entry in that dict to support another language.

## Build the index

```bash
python scripts/build_index.py        # all languages
python scripts/build_index.py asm    # just one
```

Re-run this any time you add/change files in `knowledge/`.

## Run

```bash
uvicorn app.main:app --reload
```

## Use

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What script is Khasi written in?", "language": "kha"}'
```

Response:
```json
{
  "answer": "...",
  "language": "kha",
  "sources": [{"text": "...", "score": 0.83}]
}
```

`GET /health` returns supported languages.

## Notes

- `paraphrase-multilingual-MiniLM-L12-v2` is a general multilingual model, so retrieval may be weak for rare languages. Better model by changing `EMBEDDING_MODEL` in `.env`.
- Add more languages by creating `knowledge/<code>/`, adding the code to
  `SUPPORTED_LANGUAGES` in `app/config.py`, then rebuilding the index.
