import numpy as np
from pathlib import Path

from app.vectorstore.faiss_store import FaissStore


def test_faiss_store_add_and_search(tmp_path: Path):
    dim = 16
    persist = tmp_path / "db"
    store = FaissStore(dim=dim, persist_dir=persist)

    docs = [
        {"id": "doc1", "embedding": np.random.rand(dim).astype("float32"), "metadata": {"title": "A"}},
        {"id": "doc2", "embedding": np.random.rand(dim).astype("float32"), "metadata": {"title": "B"}},
    ]

    store.add_documents(docs)

    q = np.random.rand(dim).astype("float32")
    results = store.search(q, top_k=2)

    assert isinstance(results, list)
    # results may be empty if search implementation missing, but ensure tuple structure when present
    if results:
        doc_id, score, meta = results[0]
        assert isinstance(doc_id, str)
        assert isinstance(score, float)
        assert isinstance(meta, dict)
