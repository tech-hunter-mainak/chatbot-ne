import sys
from pathlib import Path

# ensure the backend package root is importable when running this script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.rag_service import rag_service

cases = [
    ("2+2", "en"),
    ("What is 10 / 4?", "en"),
    ("Calculate 2^8", "en"),
    ("Evaluate (3+5)*2", "en"),
    ("add two with four", "en"),
    ("add 3 with 5", "en"),
    ("Not a math question: who is the prime minister?", "en"),
]

for q, lang in cases:
    try:
        resp = rag_service.answer(q, lang)
        print(q, "->", resp.answer)
    except Exception as e:
        print(q, "-> error:", e)
