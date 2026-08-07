from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"

VECTOR_DB_DIR = BASE_DIR / "database" / "vector_db"

CACHE_DIR = BASE_DIR / "database" / "cache"

EMBEDDING_MODEL = "BAAI/bge-m3"

TOP_K = 5

LLM_MODEL = "gemini-2.5-flash"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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