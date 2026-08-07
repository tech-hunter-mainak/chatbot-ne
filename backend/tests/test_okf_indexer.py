import yaml
import numpy as np
from pathlib import Path

from app.services.okf_indexer import OKFIndexer


class DummyEmbedding:
    def __init__(self):
        self.dim = 128

    def buildDocumentText(self, document):
        return f"{document.title} {document.summary}"

    def generateEmbedding(self, text):
        return np.random.rand(self.dim).astype("float32")


def make_okf_file(path: Path):
    data = {
        "id": "doc-1",
        "language": "asm",
        "category": "health",
        "title": "Health Services",
        "summary": "A summary",
        "content": "Full content",
        "keywords": ["health"],
        "tags": [],
        "source": {"name": "local"},
        "references": [],
        "last_updated": "2026-01-01"
    }

    path.mkdir(parents=True, exist_ok=True)
    with open(path / "doc1.yaml", "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh)


def test_okf_indexer_indexes_and_searches(tmp_path: Path, monkeypatch):
    # prepare knowledge dir
    kd = tmp_path / "knowledge"
    make_okf_file(kd)

    # patch EmbeddingService used in OKFIndexer to avoid heavy model loads
    monkeypatch.setattr("app.services.okf_indexer.EmbeddingService", DummyEmbedding)

    indexer = OKFIndexer(persist_dir=tmp_path / "vector_db")
    count = indexer.index_directory(kd)

    assert count == 1

    results = indexer.search("health services", top_k=3)
    assert isinstance(results, list)
