"""
Build (or rebuild) the FAISS index for one or all languages.

Usage:
    python scripts/build_index.py            # rebuild all languages
    python scripts/build_index.py asm        # rebuild only Assamese
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # allow `import app.*`

from app.config import KNOWLEDGE_DIR, SUPPORTED_LANGUAGES
from app.services.embedding_service import embedding_service
from app.services.retrieval_service import chunk_text
from app.vectorstore.faiss_manager import FaissManager


def build_language(lang: str):
    lang_dir = KNOWLEDGE_DIR / lang
    if not lang_dir.exists():
        print(f"[skip] no knowledge folder for '{lang}' ({lang_dir})")
        return

    files = list(lang_dir.glob("*.txt"))
    if not files:
        print(f"[skip] no .txt files found in {lang_dir}")
        return

    all_chunks = []
    for file in files:
        text = file.read_text(encoding="utf-8")
        all_chunks.extend(chunk_text(text))

    if not all_chunks:
        print(f"[skip] no content extracted for '{lang}'")
        return

    print(f"[{lang}] embedding {len(all_chunks)} chunks from {len(files)} file(s)...")
    vectors = embedding_service.encode(all_chunks)

    manager = FaissManager(lang)
    manager.build(vectors, all_chunks)
    print(f"[{lang}] index saved.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    languages = [target] if target else list(SUPPORTED_LANGUAGES)

    for code in languages:
        if code not in SUPPORTED_LANGUAGES:
            print(f"[error] unknown language code '{code}'. Supported: {list(SUPPORTED_LANGUAGES)}")
            continue
        build_language(code)
