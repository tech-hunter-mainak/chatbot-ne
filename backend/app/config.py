import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent          # backend/
KNOWLEDGE_DIR = BASE_DIR / "knowledge"                       # backend/knowledge/<lang>/*.txt
VECTOR_DB_DIR = BASE_DIR / "database" / "vector_db"           # backend/database/vector_db/<lang>.*
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# supported language codes -> match knowledge/<code>/ folders
SUPPORTED_LANGUAGES = {
    "asm": "Assamese",
    "kha": "Khasi",
    "grt": "Garo",
    "lus": "Mizo",
    "nag": "Nagamese",
    "trp": "Kokborok",
    "ccp": "Chakma",
    "wao": "Wancho"
}

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")

# Local, free LLM via Ollama (https://ollama.com) — no API key, no per-token cost.
# `ollama pull llama3.2` (or any model you prefer) before first run.
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

CHUNK_SIZE = 500       # chars
CHUNK_OVERLAP = 80
TOP_K = 4
